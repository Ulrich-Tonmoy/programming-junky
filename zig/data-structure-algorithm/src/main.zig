const std = @import("std");

pub fn main() !void {
    {
        std.debug.print("Loop\n", .{});
        {
            std.debug.print("For Loop: Array\n", .{});

            var array = [_]i32{ 1, 2, 3, 4, 5, 6, 7, 8 };

            for (&array) |*val| {
                val.* = 10;
                std.log.info("Slice is : {}", .{val.*});
            }
        }

        {
            std.debug.print("For Loop: Index\n", .{});

            for (0..10) |i| {
                std.log.info("i : {}", .{i});
            }
        }

        {
            std.debug.print("For Loop: Array Index\n", .{});

            var array = [_]i32{ 1, 2, 3, 4, 5, 6, 7, 8 };
            var array2 = [_]i32{ 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 };

            for (array, array2[0..array.len], 0..) |val, val2, i| {
                std.log.info("Index: {} - Value: {} - Value2: {}", .{ i, val, val2 });
            }
        }
    }

    {
        std.log.info("? - Optionals\n", .{});

        // var b: ?i32 = 4;
        var b: ?i32 = null;
        // var c: i32 = b orelse 0;
        var c: i32 = if (b) |val| val else 0;

        std.log.info("c: {}\n", .{c});

        std.log.info("if with optional capture\n", .{});

        if (b) |val| {
            std.log.info("b is not null b: {}", .{val});
        } else {
            std.log.info("b is null", .{});
        }
    }

    {
        std.log.info("Pointers*\n", .{});

        var a: i32 = 32;
        var aPtr = &a;

        std.log.info("a: {}\n", .{a});
        aPtr.* = 5;
        std.log.info("a: {}\n", .{a});

        const StructPtr = struct {
            ptr: ?*i32 = null,
        };

        var str = StructPtr{ .ptr = &a };
        std.log.info("struct value: {}", .{str.ptr.?.*});

        var ptr: [*c]i32 = &a;
        std.log.info("{} == {}", .{ ptr[0], ptr.* });

        var arr = [_]i32{ 1, 2, 3, 4 };
        var arrPtr: [*]i32 = &arr;
        var arrPtrC: [*c]i32 = &arr;
        std.log.info("many ptr: {} - c like ptr: {}", .{ arrPtr[0], arrPtrC.* });
    }

    {
        std.log.info("Impossible Node\n", .{});

        const Node = struct {
            const Self = @This();
            parentNode: ?*Self = null,
            childNode: ?*Self = null,
            text: []const u8 = "default",
        };

        var topNode = Node{ .text = "Top" };
        var betwNode = Node{ .parentNode = &topNode, .text = "Mid" };
        var lowerNode = Node{ .parentNode = &betwNode, .text = "Low" };

        topNode.childNode = &betwNode;
        betwNode.childNode = &lowerNode;

        var child: ?*Node = &topNode;

        while (child) |nextChildPtr| {
            std.log.info("Next child is: {s}", .{nextChildPtr.*.text});

            child = nextChildPtr.childNode;
        } else {
            std.log.info("End of tree!", .{});
        }
    }
}
