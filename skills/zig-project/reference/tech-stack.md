# Zig Tech Stack

## Version Strategy

> **Use latest stable Zig. Update when stable releases.**

Zig is still pre-1.0, so tracking releases is important:
- Check [ziglang.org](https://ziglang.org/download/) for latest
- Version in `build.zig.zon` with `minimum_zig_version`

---

## Core Tools

### Zig Compiler

```bash
# Build
zig build                           # Debug build
zig build -Doptimize=ReleaseFast    # Release (speed)
zig build -Doptimize=ReleaseSafe    # Release (with safety)
zig build -Doptimize=ReleaseSmall   # Release (size)

# Run
zig build run

# Test
zig build test

# Format
zig fmt src/

# Direct compilation
zig build-exe src/main.zig
zig build-lib src/lib.zig
zig run src/main.zig
zig test src/main.zig
```

### Zig as C/C++ Compiler

```bash
# Compile C
zig cc -o output input.c
zig cc -target aarch64-linux-gnu input.c

# Compile C++
zig c++ -o output input.cpp

# With flags
zig cc -O3 -march=native -o output input.c
```

### ZLS (Zig Language Server)

```bash
# Install
# Download from https://github.com/zigtools/zls/releases

# Configure in editor (VS Code, Neovim, etc.)
# Provides: completion, diagnostics, go-to-definition
```

---

## Package Management

### Built-in Package Manager

```zig
// build.zig.zon
.{
    .name = "myapp",
    .version = "0.1.0",
    .dependencies = .{
        .zap = .{
            .url = "https://github.com/zigzap/zap/archive/v0.3.0.tar.gz",
            .hash = "1220...",
        },
    },
}
```

### Fetch Dependencies

```bash
# Fetch and show hash
zig fetch https://github.com/zigzap/zap/archive/v0.3.0.tar.gz

# Update all dependencies
zig build --fetch
```

### Alternative: zigmod

```bash
# Install zigmod
# Add dependencies in zig.mod file
zigmod fetch
```

### Package Registries

- **Zigistry**: https://zigistry.dev/
- **zig.pm**: Community packages

---

## Popular Libraries

### Web/HTTP

| Library | Description | URL |
|---------|-------------|-----|
| **zap** | Blazingly fast web framework | github.com/zigzap/zap |
| **http.zig** | HTTP client/server | github.com/karlseguin/http.zig |
| **zzz** | HTTP server | github.com/supersayen/zzz |

### Async I/O

| Library | Description |
|---------|-------------|
| **std.io** | Built-in async I/O |
| **io_uring** | Linux kernel interface (used by TigerBeetle) |

### Data Structures

| Library | Description |
|---------|-------------|
| **std.ArrayList** | Dynamic array |
| **std.HashMap** | Hash map |
| **std.BoundedArray** | Fixed-capacity array |
| **std.PriorityQueue** | Priority queue |

### JSON

```zig
const std = @import("std");
const json = std.json;

// Parse JSON
const parsed = try json.parseFromSlice(MyStruct, allocator, json_string, .{});
defer parsed.deinit();

// Stringify
var buffer: [1024]u8 = undefined;
var stream = std.io.fixedBufferStream(&buffer);
try json.stringify(my_struct, .{}, stream.writer());
```

### Compression

```zig
const std = @import("std");

// DEFLATE
const deflate = std.compress.deflate;
const gzip = std.compress.gzip;
const zlib = std.compress.zlib;
```

### Crypto

```zig
const std = @import("std");
const crypto = std.crypto;

// Hashing
const hash = crypto.hash.sha2.Sha256;
var h = hash.init(.{});
h.update(data);
const digest = h.finalResult();

// Random
var prng = std.rand.DefaultPrng.init(seed);
const random = prng.random();
```

---

## C Interop

### Linking C Libraries

```zig
// build.zig
exe.linkSystemLibrary("c");
exe.linkSystemLibrary("ssl");
exe.linkSystemLibrary("crypto");

// Add include path
exe.addIncludePath(b.path("include"));
exe.addCSourceFile(.{
    .file = b.path("src/wrapper.c"),
    .flags = &.{"-Wall", "-O2"},
});
```

### Calling C from Zig

```zig
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("mylib.h");
});

pub fn main() void {
    _ = c.printf("Hello from C\n");
    c.my_c_function();
}
```

### Exposing Zig to C

```zig
// Export function with C ABI
export fn add(a: c_int, b: c_int) c_int {
    return a + b;
}

// Generate header
// zig build-lib src/lib.zig -femit-h
```

---

## Testing Tools

### std.testing

```zig
const std = @import("std");
const testing = std.testing;

test "basic assertions" {
    try testing.expect(true);
    try testing.expectEqual(@as(i32, 5), 5);
    try testing.expectEqualStrings("hello", "hello");
    try testing.expectError(error.SomeError, failingFn());
}

test "memory leak detection" {
    // testing.allocator detects leaks
    const allocator = testing.allocator;

    const ptr = try allocator.alloc(u8, 100);
    defer allocator.free(ptr);  // Must free or test fails
}

test "approximate equality" {
    try testing.expectApproxEqAbs(@as(f32, 1.0), 1.0001, 0.001);
}
```

### Test Filtering

```bash
# Run specific test
zig test src/main.zig --test-filter "my test name"

# Run tests matching pattern
zig test src/main.zig --test-filter "parse"
```

---

## Debugging

### Debug Mode

```zig
// Enabled in Debug builds
std.debug.print("Value: {}\n", .{value});
std.debug.assert(condition);

// Stack traces on panic
@panic("Something went wrong");

// Breakpoint
@breakpoint();
```

### Using GDB/LLDB

```bash
# Build with debug info (default)
zig build

# Debug
gdb ./zig-out/bin/myapp
lldb ./zig-out/bin/myapp
```

### Safety Checks

```zig
// In Debug and ReleaseSafe:
// - Array bounds checking
// - Integer overflow detection
// - Null pointer checks
// - Use-after-free detection (with testing.allocator)

const arr = [_]i32{ 1, 2, 3 };
_ = arr[10];  // Panic in safe modes
```

---

## Build Optimization

### Optimize Modes

| Mode | Speed | Safety | Size |
|------|-------|--------|------|
| Debug | Slow | Full | Large |
| ReleaseSafe | Fast | Full | Medium |
| ReleaseFast | Fastest | None | Medium |
| ReleaseSmall | Fast | None | Smallest |

### Profile-Guided Optimization

```bash
# Generate profile
zig build -Doptimize=ReleaseFast
./zig-out/bin/myapp  # Run with real workload

# Build with PGO (if using LLVM backend)
# Zig's self-hosted backend doesn't support PGO yet
```

---

## Cross-Platform Targets

### Supported Targets

```bash
# List all targets
zig targets

# Common targets
x86_64-linux-gnu
x86_64-linux-musl
aarch64-linux-gnu
x86_64-macos
aarch64-macos
x86_64-windows-msvc
x86_64-windows-gnu
wasm32-wasi
```

### Cross-Compile Example

```bash
# Build for all platforms from any machine
zig build -Dtarget=x86_64-linux-musl      # Static Linux
zig build -Dtarget=aarch64-macos          # Apple Silicon
zig build -Dtarget=x86_64-windows-gnu     # Windows
```

---

## IDE Support

### VS Code
- Extension: **Zig Language** (ziglang.vscode-zig)
- Requires ZLS installed

### Neovim
- Plugin: **nvim-lspconfig** with ZLS
- **zig.vim** for syntax

### Other Editors
- Emacs: zig-mode
- Sublime: Zig package
- IntelliJ: Zig plugin (community)
