# Zig Design Patterns

## Explicit Allocator Pattern

The fundamental Zig pattern: pass allocators explicitly.

### Basic Usage

```zig
const std = @import("std");

pub fn createBuffer(allocator: std.mem.Allocator, size: usize) ![]u8 {
    return allocator.alloc(u8, size);
}

pub fn freeBuffer(allocator: std.mem.Allocator, buffer: []u8) void {
    allocator.free(buffer);
}

// Usage
pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const buffer = try createBuffer(allocator, 1024);
    defer freeBuffer(allocator, buffer);

    // Use buffer...
}
```

### Struct with Allocator

```zig
const std = @import("std");

pub const ArrayList = struct {
    allocator: std.mem.Allocator,
    items: []u8,
    capacity: usize,

    pub fn init(allocator: std.mem.Allocator) ArrayList {
        return .{
            .allocator = allocator,
            .items = &[_]u8{},
            .capacity = 0,
        };
    }

    pub fn deinit(self: *ArrayList) void {
        if (self.capacity > 0) {
            self.allocator.free(self.items.ptr[0..self.capacity]);
        }
        self.* = undefined;
    }

    pub fn append(self: *ArrayList, item: u8) !void {
        if (self.items.len >= self.capacity) {
            try self.grow();
        }
        self.items.ptr[self.items.len] = item;
        self.items.len += 1;
    }

    fn grow(self: *ArrayList) !void {
        const new_cap = if (self.capacity == 0) 8 else self.capacity * 2;
        const new_mem = try self.allocator.realloc(
            self.items.ptr[0..self.capacity],
            new_cap,
        );
        self.items.ptr = new_mem.ptr;
        self.capacity = new_cap;
    }
};
```

---

## Arena Allocator Pattern

Bulk allocation with single deallocation. Perfect for request-scoped work.

```zig
const std = @import("std");

fn handleRequest(base_allocator: std.mem.Allocator, request: Request) !Response {
    // Create arena for this request
    var arena = std.heap.ArenaAllocator.init(base_allocator);
    defer arena.deinit();  // Frees ALL allocations at once

    const allocator = arena.allocator();

    // All allocations use arena - no individual frees needed
    const parsed = try parseRequest(allocator, request);
    const result = try processData(allocator, parsed);
    const response = try formatResponse(allocator, result);

    return response;
    // arena.deinit() cleans up everything
}
```

### Nested Arenas

```zig
fn processLargeDataset(allocator: std.mem.Allocator, data: []const Item) !Result {
    var results = std.ArrayList(ItemResult).init(allocator);
    defer results.deinit();

    for (data) |item| {
        // Inner arena for each item
        var item_arena = std.heap.ArenaAllocator.init(allocator);
        defer item_arena.deinit();

        const item_alloc = item_arena.allocator();
        const processed = try processItem(item_alloc, item);
        try results.append(processed.toResult());
        // item_arena freed, but results kept
    }

    return results.toOwnedSlice();
}
```

---

## Error Handling Patterns

### Specific Error Sets

```zig
// Define specific errors for your domain
pub const ConfigError = error{
    FileNotFound,
    ParseError,
    InvalidValue,
    MissingField,
};

pub const NetworkError = error{
    ConnectionFailed,
    Timeout,
    ProtocolError,
};

// Combine error sets
pub const AppError = ConfigError || NetworkError || error{OutOfMemory};

fn loadConfig(path: []const u8) ConfigError!Config {
    // ...
}

fn connect(host: []const u8) NetworkError!Connection {
    // ...
}
```

### errdefer for Cleanup

```zig
fn createResource(allocator: std.mem.Allocator) !*Resource {
    const resource = try allocator.create(Resource);
    errdefer allocator.destroy(resource);  // Cleanup on error

    resource.buffer = try allocator.alloc(u8, 1024);
    errdefer allocator.free(resource.buffer);

    resource.handle = try openHandle();
    errdefer closeHandle(resource.handle);

    try resource.initialize();

    return resource;  // Success - no errdefer triggered
}
```

### Error Payload (Zig 0.14+)

```zig
const ValidationError = error{
    InvalidField,
    MissingRequired,
};

fn validate(data: Data) ValidationError!void {
    if (data.name.len == 0) {
        // Can't attach payload in stable Zig yet
        // Future: return error.MissingRequired.{ .field = "name" };
        return error.MissingRequired;
    }
}
```

---

## Comptime Patterns

### Generic Container

```zig
pub fn BoundedArray(comptime T: type, comptime capacity: usize) type {
    return struct {
        const Self = @This();

        buffer: [capacity]T = undefined,
        len: usize = 0,

        pub fn append(self: *Self, item: T) !void {
            if (self.len >= capacity) {
                return error.Overflow;
            }
            self.buffer[self.len] = item;
            self.len += 1;
        }

        pub fn slice(self: *Self) []T {
            return self.buffer[0..self.len];
        }
    };
}

// Usage
var arr = BoundedArray(u32, 100){};
try arr.append(42);
```

### Type Introspection

```zig
fn printFields(comptime T: type, value: T) void {
    const info = @typeInfo(T);
    switch (info) {
        .Struct => |s| {
            inline for (s.fields) |field| {
                std.debug.print("{s}: {}\n", .{
                    field.name,
                    @field(value, field.name),
                });
            }
        },
        else => @compileError("Expected struct"),
    }
}

const Point = struct { x: i32, y: i32 };
printFields(Point, .{ .x = 10, .y = 20 });
// Output: x: 10
//         y: 20
```

### Compile-Time Validation

```zig
fn ensureValidConfig(comptime config: Config) void {
    if (config.buffer_size == 0) {
        @compileError("buffer_size must be > 0");
    }
    if (config.max_connections > 10000) {
        @compileError("max_connections too high");
    }
}

pub fn Server(comptime config: Config) type {
    ensureValidConfig(config);

    return struct {
        // Server implementation using config
    };
}
```

### Compile-Time String Operations

```zig
fn comptimeConcat(comptime a: []const u8, comptime b: []const u8) []const u8 {
    return a ++ b;
}

const greeting = comptimeConcat("Hello, ", "World!");
// greeting is "Hello, World!" at compile time
```

---

## defer Pattern

### Resource Cleanup

```zig
fn processFile(path: []const u8) !void {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();  // Always runs

    const buffer = try allocator.alloc(u8, 4096);
    defer allocator.free(buffer);

    // Use file and buffer...
    // Both cleaned up when function exits
}
```

### Multiple defers (LIFO order)

```zig
fn example() void {
    defer std.debug.print("3\n", .{});
    defer std.debug.print("2\n", .{});
    defer std.debug.print("1\n", .{});
}
// Output: 1, 2, 3 (reverse order)
```

### defer vs errdefer

```zig
fn createPair(allocator: std.mem.Allocator) !Pair {
    const a = try allocator.create(A);
    errdefer allocator.destroy(a);  // Only on error

    const b = try allocator.create(B);
    // No errdefer needed - a will be in returned Pair

    return Pair{ .a = a, .b = b };
}
```

---

## Iterator Pattern

### Simple Iterator

```zig
const Iterator = struct {
    data: []const u8,
    index: usize = 0,

    pub fn next(self: *Iterator) ?u8 {
        if (self.index >= self.data.len) return null;
        defer self.index += 1;
        return self.data[self.index];
    }
};

// Usage
var iter = Iterator{ .data = "hello" };
while (iter.next()) |char| {
    std.debug.print("{c}", .{char});
}
```

### Generic Iterator

```zig
pub fn SliceIterator(comptime T: type) type {
    return struct {
        const Self = @This();

        slice: []const T,
        index: usize = 0,

        pub fn next(self: *Self) ?T {
            if (self.index >= self.slice.len) return null;
            defer self.index += 1;
            return self.slice[self.index];
        }

        pub fn reset(self: *Self) void {
            self.index = 0;
        }
    };
}
```

---

## Interface Pattern (Duck Typing)

Zig uses comptime duck typing instead of interfaces.

```zig
fn serialize(writer: anytype, data: anytype) !void {
    // writer must have a write method
    try writer.writeAll(@typeName(@TypeOf(data)));
    try writer.writeAll(": ");

    const info = @typeInfo(@TypeOf(data));
    switch (info) {
        .Int => try writer.print("{d}", .{data}),
        .Float => try writer.print("{d:.2}", .{data}),
        .Pointer => |ptr| {
            if (ptr.child == u8) {
                try writer.writeAll(data);
            }
        },
        else => try writer.writeAll("(unknown)"),
    }
}

// Works with any type that has writeAll and print
var buffer: [256]u8 = undefined;
var stream = std.io.fixedBufferStream(&buffer);
try serialize(stream.writer(), 42);
try serialize(stream.writer(), "hello");
```

---

## Sentinel-Terminated Arrays

```zig
// Null-terminated string (C compatible)
const c_string: [:0]const u8 = "hello";

// Custom sentinel
const arr: [5:0]u8 = .{ 1, 2, 3, 4, 5 };
// arr[5] == 0 (sentinel)

// Convert to C pointer
fn toCString(s: [:0]const u8) [*:0]const u8 {
    return s.ptr;
}
```

---

## Optional Pattern

```zig
fn find(haystack: []const u8, needle: u8) ?usize {
    for (haystack, 0..) |c, i| {
        if (c == needle) return i;
    }
    return null;
}

// Usage
if (find("hello", 'l')) |index| {
    std.debug.print("Found at {}\n", .{index});
} else {
    std.debug.print("Not found\n", .{});
}

// With orelse
const index = find("hello", 'x') orelse 0;

// Unwrap (panic if null)
const index2 = find("hello", 'l').?;
```

---

## Tagged Union Pattern

```zig
const Value = union(enum) {
    int: i64,
    float: f64,
    string: []const u8,
    none,

    pub fn format(
        self: Value,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt;
        _ = options;
        switch (self) {
            .int => |v| try writer.print("{d}", .{v}),
            .float => |v| try writer.print("{d:.2}", .{v}),
            .string => |v| try writer.print("\"{s}\"", .{v}),
            .none => try writer.writeAll("null"),
        }
    }
};

// Usage
const values = [_]Value{
    .{ .int = 42 },
    .{ .float = 3.14 },
    .{ .string = "hello" },
    .none,
};

for (values) |v| {
    std.debug.print("{}\n", .{v});
}
```

---

## Summary Table

| Pattern | Use Case |
|---------|----------|
| Explicit Allocator | All memory allocation |
| Arena Allocator | Request/phase-scoped memory |
| errdefer | Cleanup on error paths |
| Comptime Generics | Type-safe containers |
| Type Introspection | Serialization, debugging |
| defer | Resource cleanup |
| Iterator | Sequential access |
| Duck Typing | Generic functions |
| Tagged Union | Sum types, variants |
| Optional | Nullable values |
