const std = @import("std");

/// Error set for library operations
pub const LibError = error{
    InvalidInput,
    FormatError,
};

/// Creates a greeting string. Caller owns returned memory.
pub fn createGreeting(allocator: std.mem.Allocator, name: []const u8) ![]u8 {
    if (name.len == 0) {
        return LibError.InvalidInput;
    }

    return std.fmt.allocPrint(allocator, "Hello, {s}!", .{name});
}

/// Example struct with explicit allocator
pub const Buffer = struct {
    allocator: std.mem.Allocator,
    data: []u8,

    pub fn init(allocator: std.mem.Allocator, size: usize) !Buffer {
        const data = try allocator.alloc(u8, size);
        return .{
            .allocator = allocator,
            .data = data,
        };
    }

    pub fn deinit(self: *Buffer) void {
        self.allocator.free(self.data);
        self.* = undefined;
    }

    pub fn fill(self: *Buffer, value: u8) void {
        @memset(self.data, value);
    }
};

// Tests

test "createGreeting with valid name" {
    const allocator = std.testing.allocator;

    const greeting = try createGreeting(allocator, "Zig");
    defer allocator.free(greeting);

    try std.testing.expectEqualStrings("Hello, Zig!", greeting);
}

test "createGreeting with empty name returns error" {
    const allocator = std.testing.allocator;

    const result = createGreeting(allocator, "");
    try std.testing.expectError(LibError.InvalidInput, result);
}

test "Buffer init and deinit" {
    const allocator = std.testing.allocator;

    var buffer = try Buffer.init(allocator, 1024);
    defer buffer.deinit();

    try std.testing.expect(buffer.data.len == 1024);
}

test "Buffer fill" {
    const allocator = std.testing.allocator;

    var buffer = try Buffer.init(allocator, 4);
    defer buffer.deinit();

    buffer.fill(0xAB);

    try std.testing.expectEqualSlices(u8, &[_]u8{ 0xAB, 0xAB, 0xAB, 0xAB }, buffer.data);
}
