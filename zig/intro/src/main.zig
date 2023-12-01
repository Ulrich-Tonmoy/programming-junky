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

            const array = [_]i32{ 1, 2, 3, 4, 5, 6, 7, 8 };
            var array2 = [_]i32{ 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 };

            for (array, array2[0..array.len], 0..) |val, val2, i| {
                std.log.info("Index: {} - Value: {} - Value2: {}", .{ i, val, val2 });
            }
        }
    }

    {
        std.log.info("? - Optionals\n", .{});

        // var b: ?i32 = 4;
        const b: ?i32 = null;
        // var c: i32 = b orelse 0;
        const c: i32 = if (b) |val| val else 0;

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
        const aPtr = &a;

        std.log.info("a: {}\n", .{a});
        aPtr.* = 5;
        std.log.info("a: {}\n", .{a});

        const StructPtr = struct {
            ptr: ?*i32 = null,
        };

        const str = StructPtr{ .ptr = &a };
        std.log.info("struct value: {}", .{str.ptr.?.*});

        const ptr: [*c]i32 = &a;
        std.log.info("{} == {}", .{ ptr[0], ptr.* });

        var arr = [_]i32{ 1, 2, 3, 4 };
        const arrPtr: [*]i32 = &arr;
        const arrPtrC: [*c]i32 = &arr;
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

    {
        std.log.info("Heap Allocator", .{});
        var alloc = std.heap.page_allocator;
        const intPtr = try alloc.create(i32);
        intPtr.* = 42;
        std.log.info("Heap allocated int is: {}", .{intPtr.*});

        std.log.info("Array List Allocator", .{});
        var list = std.ArrayList(i32).init(alloc);
        defer list.deinit();

        try list.append(4);
        try list.append(8);
        try list.append(12);
        try list.append(99);

        // remove first element and move the last to first position
        // _ = list.swapRemove(1);
        // remove first element
        _ = list.orderedRemove(0);
        // remove last element
        // _ = list.pop();

        for (list.items) |value| {
            std.log.info("value: {}", .{value});
        }
    }

    {
        std.log.info("No Constructor Destructor ->", .{});

        const Struct = struct {
            a: i32 = 0,
            info: []const u8 = "default",

            const Self = @This();

            const Error = error{
                NotEven,
            };

            fn init(self: *Self, num: i32) !void {
                if (@mod(num, 2) == 1)
                    return Error.NotEven;

                self.*.a = num;
            }

            fn deinit(self: *Self) void {
                self.*.a = 0;
            }

            fn log(self: Self) void {
                std.log.info("Struct: {} - {s}", .{ self.a, self.info });
            }
        };
        var str = Struct{};
        try str.init(12);
        defer str.deinit();
        str.log();
    }

    {
        var buffer: [64]u8 = undefined;
        var alloc = std.heap.FixedBufferAllocator.init(&buffer);

        var list = std.ArrayList(i32).init(alloc.allocator());
        defer list.deinit();

        try list.append(0);
        try list.append(5);
        try list.append(55);
        try list.append(40);

        for (list.items) |value| {
            std.log.info("Fixed buffer value: {}", .{value});
        }
    }

    {
        std.log.info("GPA ->", .{});
        var gpa = std.heap.GeneralPurposeAllocator(.{}){};
        const alloc = gpa.allocator();
        defer _ = gpa.deinit();

        {
            var list = std.ArrayList(i32).init(alloc);
            defer list.deinit();

            try list.append(0);
            try list.append(5);
            try list.append(55);
            try list.append(40);

            for (list.items) |value| {
                std.log.info("Fixed buffer value: {}", .{value});
            }
        }

        const aPtr = try alloc.create(i32);
        aPtr.* = 10;
        alloc.destroy(aPtr);
    }

    {
        std.log.info("No Operator Overloads ->", .{});

        const Vec3 = struct {
            x: f32,
            y: f32,
            z: f32,

            const Self = @This();

            fn dot(self: Self, other: Self) f32 {
                return self.x * other.x + self.y * other.y * self.z * other.z;
            }
        };

        var vec = Vec3{ .x = 1, .y = 2, .z = 1 };
        const vec2 = vec;
        const dotProduct = vec.dot(vec2);
        std.log.info("dot product: {}", .{dotProduct});
    }

    {
        std.log.info("Vector ->", .{});

        const a: f32 = 12;
        const b: f64 = 10;
        const sum = a + b;
        std.log.info("sum: {d:.2} - {}", .{ sum, @TypeOf(sum) });

        const vec1 = @Vector(3, f32){ 1, 2, 3 };
        const vec2 = @Vector(3, f32){ 1, 4, 3 };

        const result = vec1 + vec2;
        std.log.info("vec: {d:.2}", .{result});
    }
}
