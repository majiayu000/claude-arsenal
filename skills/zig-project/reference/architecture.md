# Zig Project Architecture

## Project Layouts

### Executable Project

```
myapp/
├── build.zig           # Build configuration
├── build.zig.zon       # Package manifest
├── src/
│   ├── main.zig        # Entry point
│   ├── lib.zig         # Internal library (optional)
│   └── utils/          # Sub-modules
│       ├── math.zig
│       └── io.zig
├── tests/              # Integration tests (optional)
│   └── integration.zig
└── lib/                # Vendored C libraries (optional)
    └── stb/
```

### Library Project

```
mylib/
├── build.zig
├── build.zig.zon
├── src/
│   ├── root.zig        # Library root (exports)
│   ├── core.zig
│   └── internal/       # Private modules
│       └── helpers.zig
├── tests/
│   └── lib_test.zig
└── examples/
    └── basic.zig
```

### Application with Multiple Binaries

```
project/
├── build.zig
├── build.zig.zon
├── src/
│   ├── lib/            # Shared library code
│   │   ├── root.zig
│   │   └── core.zig
│   ├── server/         # Server binary
│   │   └── main.zig
│   ├── client/         # Client binary
│   │   └── main.zig
│   └── cli/            # CLI tool
│       └── main.zig
└── tests/
```

---

## Module System

### File = Module

Each `.zig` file is a module. No explicit module declarations needed.

```zig
// src/main.zig
const std = @import("std");
const utils = @import("utils/math.zig");  // Import from path

pub fn main() !void {
    const result = utils.add(1, 2);
    std.debug.print("Result: {}\n", .{result});
}
```

```zig
// src/utils/math.zig
pub fn add(a: i32, b: i32) i32 {
    return a + b;
}

// Private function (not exported)
fn helper() void {}
```

### Root Module Pattern

```zig
// src/root.zig (library root)
pub const core = @import("core.zig");
pub const utils = @import("utils.zig");

// Re-export commonly used items
pub const Config = core.Config;
pub const Error = core.Error;

// Top-level functions
pub fn init(allocator: std.mem.Allocator) !*Context {
    return core.Context.init(allocator);
}
```

### @import vs usingnamespace

```zig
// Prefer explicit imports
const http = @import("http.zig");
const response = http.Response;

// Avoid usingnamespace in public APIs
// Only use for private convenience
const Self = @This();
```

---

## Build System

### Basic build.zig

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    // Allow user to override target and optimize
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Main executable
    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Link system libraries if needed
    exe.linkSystemLibrary("c");
    exe.linkSystemLibrary("ssl");

    b.installArtifact(exe);

    // Run step
    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| {
        run_cmd.addArgs(args);
    }
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_cmd.step);

    // Test step
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_tests.step);
}
```

### Library Build

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Static library
    const lib = b.addStaticLibrary(.{
        .name = "mylib",
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(lib);

    // Also create module for use as dependency
    _ = b.addModule("mylib", .{
        .root_source_file = b.path("src/root.zig"),
    });
}
```

### Multiple Targets

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Server
    const server = b.addExecutable(.{
        .name = "server",
        .root_source_file = b.path("src/server/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(server);

    // Client
    const client = b.addExecutable(.{
        .name = "client",
        .root_source_file = b.path("src/client/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(client);

    // CLI
    const cli = b.addExecutable(.{
        .name = "cli",
        .root_source_file = b.path("src/cli/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(cli);

    // Shared library module
    const lib_mod = b.addModule("lib", .{
        .root_source_file = b.path("src/lib/root.zig"),
    });

    server.root_module.addImport("lib", lib_mod);
    client.root_module.addImport("lib", lib_mod);
    cli.root_module.addImport("lib", lib_mod);
}
```

---

## Package Manifest (build.zig.zon)

### Basic Manifest

```zig
.{
    .name = "myapp",
    .version = "0.1.0",

    // Minimum Zig version required
    .minimum_zig_version = "0.13.0",

    .dependencies = .{},

    // Files to include in package
    .paths = .{
        "build.zig",
        "build.zig.zon",
        "src",
        "LICENSE",
        "README.md",
    },
}
```

### With Dependencies

```zig
.{
    .name = "myapp",
    .version = "0.1.0",

    .dependencies = .{
        .zap = .{
            .url = "https://github.com/zigzap/zap/archive/refs/tags/v0.3.0.tar.gz",
            .hash = "1220aabbccdd...",
        },
        .known_folders = .{
            .url = "git+https://github.com/ietf-wg-masque/draft-ietf-masque-connect-ip#v0.1.0",
            .hash = "1220...",
        },
        // Local path dependency
        .mylib = .{
            .path = "../mylib",
        },
    },

    .paths = .{
        "build.zig",
        "build.zig.zon",
        "src",
    },
}
```

### Using Dependencies in build.zig

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Get dependency
    const zap = b.dependency("zap", .{
        .target = target,
        .optimize = optimize,
    });

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Add dependency module
    exe.root_module.addImport("zap", zap.module("zap"));

    b.installArtifact(exe);
}
```

---

## TigerBeetle-Style Architecture

For high-performance, safety-critical systems:

```
project/
├── build.zig
├── build.zig.zon
├── src/
│   ├── main.zig              # Entry point
│   ├── state_machine.zig     # Core FSM
│   ├── io.zig                # I/O layer (io_uring)
│   ├── storage.zig           # Storage engine
│   ├── network.zig           # Network layer
│   ├── config.zig            # Static configuration
│   └── types.zig             # Fixed-size types
├── scripts/
│   └── benchmark.zig
└── clients/                   # Language bindings
    ├── zig/
    └── c/
```

### Key Principles

```zig
// types.zig - Fixed size, cache-aligned
pub const Transfer = extern struct {
    id: u128,
    debit_account: u128,
    credit_account: u128,
    amount: u64,
    timestamp: u64,
    // Exactly 128 bytes, cache-line aligned

    comptime {
        std.debug.assert(@sizeOf(Transfer) == 128);
        std.debug.assert(@alignOf(Transfer) == 64);
    }
};

// Static memory allocation
var transfers: [MAX_TRANSFERS]Transfer = undefined;
var transfer_count: usize = 0;
```

---

## Cross-Compilation

### From build.zig

```zig
pub fn build(b: *std.Build) void {
    // Let user override, with defaults
    const target = b.standardTargetOptions(.{
        .default_target = .{
            .cpu_arch = .x86_64,
            .os_tag = .linux,
            .abi = .gnu,
        },
    });

    // ...
}
```

### From Command Line

```bash
# Linux x86_64
zig build -Dtarget=x86_64-linux-gnu

# macOS ARM64
zig build -Dtarget=aarch64-macos

# Windows x86_64
zig build -Dtarget=x86_64-windows-msvc

# FreeBSD
zig build -Dtarget=x86_64-freebsd

# Cross-compile C code
zig cc -target aarch64-linux-gnu -o output input.c
```

---

## Test Organization

### Inline Tests (Recommended)

```zig
// src/math.zig
const std = @import("std");

pub fn add(a: i32, b: i32) i32 {
    return a + b;
}

pub fn divide(a: i32, b: i32) !i32 {
    if (b == 0) return error.DivisionByZero;
    return @divTrunc(a, b);
}

// Tests are in the same file
test "add works" {
    try std.testing.expectEqual(@as(i32, 5), add(2, 3));
}

test "divide by zero returns error" {
    try std.testing.expectError(error.DivisionByZero, divide(10, 0));
}

test "divide works" {
    try std.testing.expectEqual(@as(i32, 5), try divide(10, 2));
}
```

### Separate Test Files

```zig
// tests/integration.zig
const std = @import("std");
const mylib = @import("mylib");

test "full integration test" {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var app = try mylib.App.init(allocator);
    defer app.deinit();

    try app.run();
}
```

Add to build.zig:
```zig
const integration_tests = b.addTest(.{
    .root_source_file = b.path("tests/integration.zig"),
    .target = target,
    .optimize = optimize,
});
integration_tests.root_module.addImport("mylib", lib_mod);

const run_integration = b.addRunArtifact(integration_tests);
const integration_step = b.step("test-integration", "Run integration tests");
integration_step.dependOn(&run_integration.step);
```
