import add
import math

# dimensions
TOTAL  = 100  # total ground size
WATER_W = 80  # water width  (x)
WATER_D = 80  # water depth  (z)
margin = (TOTAL - WATER_W) // 2  # sand border width = 25

WATER_COLOR = [50, 130, 200]
SAND_COLOR  = [255, 216, 110]

def make_flat(x_off, z_off):
    def f(u, v): return [x_off + u, 0, z_off + v]
    return f

# water (y=0.1 so it sits just above sand)
def water(u, v): return [margin + u, 0.1, margin + v]
add.parametric(water, 0, WATER_W, 100, 0, WATER_D, 100, WATER_COLOR)

# sand: 4 strips around the water
add.parametric(make_flat(0,                    0),          0, TOTAL,   50, 0, margin,  50, SAND_COLOR)  # front strip
add.parametric(make_flat(0,        margin+WATER_D),          0, TOTAL,   50, 0, margin,  50, SAND_COLOR)  # back strip
add.parametric(make_flat(0,               margin),          0, margin,  50, 0, WATER_D, 50, SAND_COLOR)  # left strip
add.parametric(make_flat(margin+WATER_W,  margin),          0, margin,  50, 0, WATER_D, 50, SAND_COLOR)  # right strip

# octopus head
HEAD_COLOR  = [179, 0, 0]
BODY_COLOR  = [179, 0, 0]
NUM_LEGS    = 100  # parameter - controls number of tentacles

add.sphere([50, 8, 50], 8, 15, HEAD_COLOR)

# body strips - two segments per strip for a curved silhouette
def make_strip_seg(sx, sy, sz, ex, ey, ez, w, angle):
    px = -math.sin(angle)
    pz =  math.cos(angle)
    def f(u, v):
        return [sx + (ex-sx)*u + px*v*w,
                sy + (ey-sy)*u,
                sz + (ez-sz)*u + pz*v*w]
    return f

for i in range(NUM_LEGS):
    angle = i * 2 * math.pi / NUM_LEGS
    cx, cy, cz = 50, 8, 50
    r = 8
    w = 1.0
    sx = cx + r * math.cos(angle)
    sz = cz + r * math.sin(angle)

    # segment 1: steep inward (top, near sphere)
    shift1 = 4 * math.tan(math.radians(8))
    mx = sx - math.cos(angle) * shift1
    my = 4
    mz = sz - math.sin(angle) * shift1

    # segment 2: shallow angle (bottom, near water)
    shift2 = 3.8 * math.tan(math.radians(13))
    ex = mx - math.cos(angle) * shift2
    ey = 0.2
    ez = mz - math.sin(angle) * shift2

    add.parametric(make_strip_seg(sx, cy, sz, mx, my, mz, w, angle), 0, 1, 10, -1, 1, 5, BODY_COLOR)
    add.parametric(make_strip_seg(mx, my, mz, ex, ey, ez, w, angle), 0, 1, 10, -1, 1, 5, BODY_COLOR)

# tentacles
TENTACLE_COLOR = [179, 0, 0]
TENTACLE_TIP   = [232, 67, 67]
CUP_COLOR      = [120, 0, 0]
NUM_TENTACLES  = 8   # parameter - controls number of tentacles
start_r        = 13  # distance from center where tentacles begin
sw             = 0.6 # stripe width in radians

def make_tentacle_seg(bx, by, bz, lean_x, lean_z, height, r_base, r_top, r_offset=0):
    def f(u, v):
        r  = r_base + (r_top - r_base) * u + r_offset
        cx = bx + lean_x * u
        cy = by + height  * u
        cz = bz + lean_z  * u
        return [cx + r * math.cos(v), cy, cz + r * math.sin(v)]
    return f

def add_tentacle(a):
    # base of segment 1
    bx1 = 50 + start_r * math.cos(a)
    bz1 = 50 + start_r * math.sin(a)
    # lean outward from head
    l1x = 3 * math.cos(a);  l1z = 3 * math.sin(a)
    l2x = 7 * math.cos(a);  l2z = 7 * math.sin(a)
    # base of segment 2 (tip of segment 1)
    bx2 = bx1 + l1x;  bz2 = bz1 + l1z
    # tip of segment 2
    tx = bx2 + l2x;   tz = bz2 + l2z

    # body
    add.parametric(make_tentacle_seg(bx1, 0, bz1, l1x, l1z, 12, 2.0, 1.5),        0, 1, 20, 0, 2*math.pi, 20, TENTACLE_COLOR)
    add.parametric(make_tentacle_seg(bx2, 12, bz2, l2x, l2z, 12, 1.5, 0.25),      0, 1, 20, 0, 2*math.pi, 20, TENTACLE_COLOR)
    # stripe
    add.parametric(make_tentacle_seg(bx1, 0, bz1, l1x, l1z, 12, 2.0, 1.5,  0.05), 0, 1, 20, a-sw, a+sw, 5, TENTACLE_TIP)
    add.parametric(make_tentacle_seg(bx2, 12, bz2, l2x, l2z, 12, 1.5, 0.25, 0.05), 0, 1, 20, a-sw, a+sw, 5, TENTACLE_TIP)
    # tip sphere
    add.sphere([tx, 24, tz], 0.25, 5, TENTACLE_COLOR)

    # suction cups - segment 1
    for i in range(6):
        u  = (i + 0.5) / 6
        r  = 2 + (1.5 - 2) * u
        cx = bx1 + l1x * u;  cz = bz1 + l1z * u;  cy = 12 * u
        sx = cx + (r + 0.4) * math.cos(a);  sz = cz + (r + 0.4) * math.sin(a)
        ex = cx + (r - 0.2) * math.cos(a);  ez = cz + (r - 0.2) * math.sin(a)
        add.cone([sx, cy, sz], [ex, cy, ez], 0.35, 10, CUP_COLOR)
    # suction cups - segment 2
    for i in range(5):
        u  = (i + 0.5) / 5
        r  = 1.5 + (0.25 - 1.5) * u
        cx = bx2 + l2x * u;  cz = bz2 + l2z * u;  cy = 12 + 12 * u
        sx = cx + (r + 0.4) * math.cos(a);  sz = cz + (r + 0.4) * math.sin(a)
        ex = cx + (r - 0.2) * math.cos(a);  ez = cz + (r - 0.2) * math.sin(a)
        add.cone([sx, cy, sz], [ex, cy, ez], 0.25, 10, CUP_COLOR)

for i in range(NUM_TENTACLES):
    add_tentacle(i * 2 * math.pi / NUM_TENTACLES)

# face :3
EYE_COLOR   = [255, 220, 0]
PUPIL_COLOR = [15, 5, 5]
MOUTH_COLOR = [100, 0, 0]

def sz(x, y, p=0.5):  # z on sphere surface + protrusion p outward
    d2 = (x-50)**2 + (y-8)**2
    return 50 - math.sqrt(max(0.01, 64 - d2)) - p

# eyes
add.sphere([47.0, 11.0, sz(47.0, 11.0)],       0.8,  8, EYE_COLOR)
add.sphere([53.0, 11.0, sz(53.0, 11.0)],       0.8,  8, EYE_COLOR)
add.rectangle3D([47.0, 11.0, sz(47.0, 11.0, 1.3)], [0.8, 0.5, 0.05], PUPIL_COLOR)
add.rectangle3D([53.0, 11.0, sz(53.0, 11.0, 1.3)], [0.8, 0.5, 0.05], PUPIL_COLOR)

# "3" mouth - two downward bumps side by side (w shape), meeting at center
def left_bump(t):   # t: 0 to pi, from center going left
    x = 48.75 + 1.25 * math.cos(t)
    y = 7.5   - 1.25 * math.sin(t)
    return [x, y, sz(x, y, 0.5)]

def right_bump(t):  # t: 0 to pi, from center going right
    x = 51.25 - 1.25 * math.cos(t)
    y = 7.5   - 1.25 * math.sin(t)
    return [x, y, sz(x, y, 0.5)]

add.curve(left_bump,  0, math.pi, 12, 6, 0.15, MOUTH_COLOR, False)
add.curve(right_bump, 0, math.pi, 12, 6, 0.15, MOUTH_COLOR, False)

# straw hat
HAT_COLOR  = [220, 185, 75]
BAND_COLOR = [200, 0, 0]

hat_y      = 14.0   # where hat sits on head
r_inner    = 6.0    # inner brim radius (matches sphere at that height)
r_outer    = 12.0    # outer brim radius
crown_h    = 7.0    # crown height
crown_rb   = 6.0    # crown base radius
crown_rt   = 5.0    # crown top radius

hat_tilt = math.radians(8)  # tilt angle toward back (+z)

def tilt_hat(x, y, z):
    dy = y - hat_y
    dz = z - 50
    return [x,
            hat_y + dy * math.cos(hat_tilt) - dz * math.sin(hat_tilt),
            50    + dy * math.sin(hat_tilt) + dz * math.cos(hat_tilt)]

# brim - droops slightly toward edges
def brim(u, v):
    r = r_inner + (r_outer - r_inner) * u
    return tilt_hat(50 + r * math.cos(v), hat_y - 1.8 * u * u, 50 + r * math.sin(v))
add.parametric(brim, 0, 1, 15, 0, 2*math.pi, 60, HAT_COLOR)

# crown - hemisphere sitting directly on brim
def crown_dome(u, v):
    return tilt_hat(50 + crown_rb * math.cos(u) * math.cos(v),
                    hat_y + crown_rb * math.sin(u),
                    50 + crown_rb * math.cos(u) * math.sin(v))
add.parametric(crown_dome, 0, math.pi/2, 15, 0, 2*math.pi, 40, HAT_COLOR)

# hat band
def band(u, v):
    return tilt_hat(50 + (crown_rb + 0.05) * math.cos(v), hat_y + 1.5 * u, 50 + (crown_rb + 0.05) * math.sin(v))
add.parametric(band, 0, 1, 3, 0, 2*math.pi, 40, BAND_COLOR)

# shadows on water surface
SHADOW_COLOR = [25, 75, 140]

def head_shadow(u, v):
    return [50 + u * 9 * math.cos(v), 0.15, 50 + u * 9 * math.sin(v)]
add.parametric(head_shadow, 0, 1, 5, 0, 2*math.pi, 50, SHADOW_COLOR)

def make_shadow(cx, cz):
    def f(u, v): return [cx + u * 2.5 * math.cos(v), 0.15, cz + u * 2.5 * math.sin(v)]
    return f

for i in range(NUM_TENTACLES):
    a  = i * 2 * math.pi / NUM_TENTACLES
    bx = 50 + start_r * math.cos(a)
    bz = 50 + start_r * math.sin(a)
    add.parametric(make_shadow(bx, bz), 0, 1, 3, 0, 2*math.pi, 20, SHADOW_COLOR)

add.off("model.off")
