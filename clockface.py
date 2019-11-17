import cairo
import math

width_mm = 155
height_mm = 155
mm_per_inch = 25.4
points_per_mm = 72 / 25.4
resolution = 300
x_pixels = int(width_mm / mm_per_inch * resolution)
y_pixels = int(height_mm / mm_per_inch * resolution)
x_points = width_mm * points_per_mm
y_points = height_mm * points_per_mm

cx = width_mm / 2
cy = height_mm / 2
cut_r = 153/2

# ticks
hour_outer_r = cut_r - 8
hour_inner_r = hour_outer_r - 4
hour_width = 3
minute_outer_r = hour_outer_r
minute_inner_r = minute_outer_r - 3
minute_width = 1

# centre hole
hole_r = 4

# label
label_r = 56
label_size = 14

# brand
brand_size = 8
brand_dy_1 = -30
brand_dy_2 = -20
brand_dy_3 = 25


def mm_to_points(mm):
    return


def centre_text(ctx, x, y, text):
    (x_bearing, y_bearing, width, height, x_advance, y_advance) = ctx.text_extents(text)
    ctx.move_to(x - width / 2, y + height / 2)
    ctx.show_text(str(text))


def clear(ctx):
    ctx.rectangle(0, 0, width_mm, height_mm)  # Rectangle(x0, y0, x1, y1)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()


def cutline(ctx):
    ctx.save()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.5)
    ctx.arc(cx, cy, cut_r, 0, 2 * math.pi)
    ctx.stroke()
    ctx.restore()


def hole(ctx):
    ctx.save()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.5)
    ctx.arc(cx, cy, hole_r, 0, 2 * math.pi)
    ctx.stroke()
    ctx.restore()


def ticks(ctx):
    ctx.save()

    ctx.set_source_rgb(0, 0, 0)

    for angle in range(0, 360, 6):
        if angle % 30:
            width = minute_width
            inner_r = minute_inner_r
            outer_r = minute_outer_r
        else:
            width = hour_width
            inner_r = hour_inner_r
            outer_r = hour_outer_r

        ctx.set_line_width(width)

        rad = math.radians(angle)
        x0 = cx + inner_r * math.sin(rad)
        y0 = cy + inner_r * math.cos(rad)
        x1 = cx + outer_r * math.sin(rad)
        y1 = cy + outer_r * math.cos(rad)
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        ctx.stroke()

    ctx.restore()


def label(ctx):
    ctx.save()

    ctx.set_source_rgb(0, 0, 0)
    ctx.select_font_face("Rockwell", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(label_size)

    for hour in range(1, 13):
        angle = math.radians(180 - hour * 30)
        x = cx + label_r * math.sin(angle)
        y = cy + label_r * math.cos(angle)
        centre_text(ctx, x, y, str(hour))
    ctx.restore()


def brand(ctx):
    ctx.save()
    ctx.set_source_rgb(0, 0, 0)
    ctx.select_font_face("Copperplate", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(brand_size)
    centre_text(ctx, cx, cy + brand_dy_1, "Excel")
    centre_text(ctx, cx, cy + brand_dy_2, "Psychology")
    centre_text(ctx, cx, cy + brand_dy_3, "Spring Hill")
    ctx.restore()


def draw(outfile):
    print(f"Writing clock face to {outfile}")

    surface = cairo.PDFSurface(outfile, x_points, y_points)
    ctx = cairo.Context(surface)
    ctx.scale(x_points/width_mm, y_points/height_mm)

    clear(ctx)
    hole(ctx)
    cutline(ctx)
    ticks(ctx)
    label(ctx)
    brand(ctx)


if __name__ == "__main__":
    draw('clockface.pdf')
