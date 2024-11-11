// Polygon class
class Polygon extends AbstractShape {
    private int numSides;
    private double radius;

    public Polygon(Point center, int numSides, double radius) {
        super(center);
        this.numSides = numSides;
        this.radius = radius;
    }

    @Override
    public double getArea() {
        return (numSides * Math.pow(radius, 2) * Math.sin(2 * Math.PI / numSides)) / 2;
    }

    @Override
    public double getPerimeter() {
        return 2 * numSides * radius * Math.sin(Math.PI / numSides);
    }

    @Override
    public boolean isPointEnclosed(Point p) {
        double angleIncrement = 2 * Math.PI / numSides;
        double angleOffset = Math.atan2(p.y - origin.y, p.x - origin.x);

        for (int i = 0; i < numSides; i++) {
            double angle1 = angleOffset + i * angleIncrement;
            double angle2 = angleOffset + (i + 1) * angleIncrement;

            Point vertex1 = new Point(
                origin.x + radius * Math.cos(angle1),
                origin.y + radius * Math.sin(angle1)
            );
            Point vertex2 = new Point(
                origin.x + radius * Math.cos(angle2),
                origin.y + radius * Math.sin(angle2)
            );

            double crossProduct = (p.x - vertex1.x) * (vertex2.y - vertex1.y) - (p.y - vertex1.y) * (vertex2.x - vertex1.x);
            if (crossProduct > 0) return false;
        }
        return true;
    }

    @Override
    public ShapeType getShapeType() {
        return ShapeType.POLYGON;
    }
}