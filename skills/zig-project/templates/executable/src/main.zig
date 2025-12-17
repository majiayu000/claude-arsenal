const std = @import("std");
const lib = @import("lib.zig");

pub fn main() !void {
    // Use GeneralPurposeAllocator for memory allocation
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Get stdout writer
    const stdout = std.io.getStdOut().writer();

    // Example: Use library function
    const greeting = try lib.createGreeting(allocator, "World");
    defer allocator.free(greeting);

    try stdout.print("{s}\n", .{greeting});
}

test "main runs without error" {
    // Basic smoke test
    const allocator = std.testing.allocator;
    const greeting = try lib.createGreeting(allocator, "Test");
    defer allocator.free(greeting);

    try std.testing.expectEqualStrings("Hello, Test!", greeting);
}
