# Homing-missile-
2D video game guided missile algorithm

1) LEAD COLLISION INTERCEPT THEOREM (Thales basic proportionality theorem
2) PURE PURSUIT ALGORITHM  

RESOURCES:
https://www.youtube.com/watch?v=T2fPKUfmnKo
https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

    In computer geometry, always use vectors if possible!
    Code gets more complicated if you try to work with Cartesian co-ordinates
    (x,y) or with line equations y=mx+b.
    Here, for example, you have special cases for horizontal lines, m=0, and vertical lines, m=∞.
    So let's try to program this, sticking to vectors throughout.
    First, let's review the problem. We have a line segment from p1.p to p2.p and we want to find
    the points of intersection with a circle centred at self.p and radius self.r. I'm going to write these as
    p1, p2, q, and r respectively.

    Any point on the line segment can be written p1+t(p2−p1)for a
    scalar parameter t between 0 and 1. We'll be using p2−p1 often, so let's write v=p2−p1.
    Let's set this up in Python. I'm assuming that all the points are pygame.math.Vector2 objects,
    so that we can add them and take dot products and so on.
    I'm also assuming that we're using Python 3, so that division returns a float

    Q is the centre of circle (pygame.math.Vector2)
    r is the radius           (scalar)
    p1 constraint.point1      (pygame.math.Vector2), start of the line segment
    v constraint.point2 - p1  (pygame.math.Vector2), vector along line segment
    Now, a point x is on the circle if its distance from the centre of the circle is equal
    to the circle's radius, that is, if
    |x - q| = r
    So the line intersects the circle when
    |p1 + tv - q| = r
    Squaring both sides gives
    |p1 + tv - q| **2 = r ** 2
    Expanding the dot product and collecting powers of t gives
    t ** 2 (v.v) + 2t(v.(p1 - q)) + (p1.p1 + q.q - 2p1.q - r**2) = 0
    which is a quadratic equation in t with coefficients
    a = v.v
    b = 2(v.(p1 - q))
    c = p1.p1 + q.q - 2p1.q - r ** 2
    and solutions
    t = (-b +/- math.sqrt(b ** 2 - 4 * a * c)) / 2 * a

    a = V.dot(V)
    b = 2 * V.dot(P1 - Q)
    c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r ** 2
    The value b2−4ac inside the square root is known as the discriminant.
    If this is negative, then there are no real solutions to the quadratic equation;
    that means that the line misses the circle entirely.

    disc = b**2 - 4 * a * c
    if disc < 0:
        return False, None

    Otherwise, let's call the two solutions t1 and t2.
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)

    If neither of these is between 0 and 1, then the line segment misses the circle (but would hit it if extended):
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
    return False, None

    Now, the closest point on the extended line to the centre of the circle is
    p1+tv where
    t= ((q−p1)⋅v) / (|v| ** 2) = −b / 2a

    But we want to ensure that the point is on the line segment, so we must clamp
    t to lie between 0 and 1.
    t = max(0, min(1, - b / (2 * a)))
    return True, P1 + t * V

    
