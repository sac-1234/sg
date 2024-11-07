import java.util.*;
import java.time.LocalDateTime;

enum ShapeType {
    CIRCLE, SQUARE, RECTANGLE, TRIANGLE, POLYGON
}

interface Shape {
    double getArea();
    double getPerimeter();
    Point getOrigin();
    boolean isPointEnclosed(Point p);
    ShapeType getShapeType();
    LocalDateTime getTimestamp();
    double distanceFromOrigin();
}

class Point {
    double x, y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distance(Point other) {
        return Math.sqrt(Math.pow(this.x - other.x, 2) + Math.pow(this.y - other.y, 2));
    }
}

abstract class AbstractShape implements Shape {
    protected Point origin;
    protected LocalDateTime timestamp;

    public AbstractShape(Point origin) {
        this.origin = origin;
        this.timestamp = LocalDateTime.now();
    }

    @Override
    public Point getOrigin() {
        return origin;
    }

    @Override
    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    @Override
    public double distanceFromOrigin() {
        return origin.distance(new Point(0, 0));
    }
}

// Circle class
class Circle extends AbstractShape {
    private double radius;

    public Circle(Point center, double radius) {
        super(center);
        this.radius = radius;
    }

    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }

    @Override
    public double getPerimeter() {
        return 2 * Math.PI * radius;
    }

    @Override
    public boolean isPointEnclosed(Point p) {
        return origin.distance(p) <= radius;
    }

    @Override
    public ShapeType getShapeType() {
        return ShapeType.CIRCLE;
    }
}

// Square class
class Square extends AbstractShape {
    private double side;

    public Square(Point origin, double side) {
        super(origin);
        this.side = side;
    }

    @Override
    public double getArea() {
        return side * side;
    }

    @Override
    public double getPerimeter() {
        return 4 * side;
    }

    @Override
    public boolean isPointEnclosed(Point p) {
        return (p.x >= origin.x && p.x <= origin.x + side) &&
               (p.y >= origin.y && p.y <= origin.y + side);
    }

    @Override
    public ShapeType getShapeType() {
        return ShapeType.SQUARE;
    }
}

// Rectangle class
class Rectangle extends AbstractShape {
    private double length, breadth;

    public Rectangle(Point origin, double length, double breadth) {
        super(origin);
        this.length = length;
        this.breadth = breadth;
    }

    @Override
    public double getArea() {
        return length * breadth;
    }

    @Override
    public double getPerimeter() {
        return 2 * (length + breadth);
    }

    @Override
    public boolean isPointEnclosed(Point p) {
        return (p.x >= origin.x && p.x <= origin.x + length) &&
               (p.y >= origin.y && p.y <= origin.y + breadth);
    }

    @Override
    public ShapeType getShapeType() {
        return ShapeType.RECTANGLE;
    }
}

// ShapeFactory class
class ShapeFactory {
    public static Shape createShape(ShapeType type, Point origin, List<Double> parameters) {
        switch (type) {
            case CIRCLE:
                return new Circle(origin, parameters.get(0));
            case SQUARE:
                return new Square(origin, parameters.get(0));
            case RECTANGLE:
                return new Rectangle(origin, parameters.get(0), parameters.get(1));
            // Add other shapes like Triangle and Polygon as needed
            default:
                throw new IllegalArgumentException("Shape type not supported.");
        }
    }
}

// Screen class
class Screen {
    private List<Shape> shapes = new ArrayList<>();

    public void addShape(Shape shape) {
        shapes.add(shape);
    }

    public void deleteShape(Shape shape) {
        shapes.remove(shape);
    }

    public void deleteShapesByType(ShapeType type) {
        shapes.removeIf(shape -> shape.getShapeType() == type);
    }

    public List<Shape> getShapesSortedBy(Comparator<Shape> comparator) {
        List<Shape> sortedShapes = new ArrayList<>(shapes);
        sortedShapes.sort(comparator);
        return sortedShapes;
    }

    public List<Shape> getShapesEnclosingPoint(Point point) {
        List<Shape> enclosingShapes = new ArrayList<>();
        for (Shape shape : shapes) {
            if (shape.isPointEnclosed(point)) {
                enclosingShapes.add(shape);
            }
        }
        return enclosingShapes;
    }

    public List<Shape> getShapesOnTopOf(Shape baseShape) {
        List<Shape> overlappingShapes = new ArrayList<>();
        for (Shape shape : shapes) {
            if (shape.getTimestamp().isAfter(baseShape.getTimestamp()) && baseShape.isPointEnclosed(shape.getOrigin())) {
                overlappingShapes.add(shape);
            }
        }
        return overlappingShapes;
    }
}

// Main class to demonstrate usage
public class GraphicsLibraryDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Screen screen = new Screen();

        while (true) {
            System.out.println("1. Add Shape");
            System.out.println("2. Delete Shape");
            System.out.println("3. Delete Shapes by Type");
            System.out.println("4. Get Sorted Shapes");
            System.out.println("5. Get Shapes Enclosing Point");
            System.out.println("6. Get Shapes On Top Of Another");
            System.out.println("7. Exit");

            int choice = scanner.nextInt();
            if (choice == 7) break;

            switch (choice) {
                case 1 -> {
                    System.out.println("Enter shape type (CIRCLE, SQUARE, RECTANGLE):");
                    ShapeType type = ShapeType.valueOf(scanner.next().toUpperCase());
                    System.out.println("Enter origin x and y:");
                    Point origin = new Point(scanner.nextDouble(), scanner.nextDouble());
                    System.out.println("Enter parameters (e.g., radius for circle, side for square, etc.):");
                    List<Double> parameters = new ArrayList<>();
                    parameters.add(scanner.nextDouble());
                    if (type == ShapeType.RECTANGLE) parameters.add(scanner.nextDouble());

                    Shape shape = ShapeFactory.createShape(type, origin, parameters);
                    screen.addShape(shape);
                    System.out.println("Shape added.");
                }
                case 2 -> {
                    System.out.println("Enter shape origin x and y:");
                    Point origin = new Point(scanner.nextDouble(), scanner.nextDouble());
                    screen.shapes.removeIf(shape -> shape.getOrigin().equals(origin));
                    System.out.println("Shape deleted.");
                }
                case 3 -> {
                    System.out.println("Enter shape type (CIRCLE, SQUARE, RECTANGLE):");
                    ShapeType type = ShapeType.valueOf(scanner.next().toUpperCase());
                    screen.deleteShapesByType(type);
                    System.out.println("Shapes deleted.");
                }
                case 4 -> {
                    System.out.println("Choose sorting criteria: 1. Area 2. Perimeter 3. Timestamp 4. Distance from Origin");
                    int sortChoice = scanner.nextInt();
                    Comparator<Shape> comparator;
                    comparator = switch (sortChoice) {
                        case 1 -> Comparator.comparingDouble(Shape::getArea);
                        case 2 -> Comparator.comparingDouble(Shape::getPerimeter);
                        case 3 -> Comparator.comparing(Shape::getTimestamp);
                        case 4 -> Comparator.comparingDouble(Shape::distanceFromOrigin);
                        default -> throw new IllegalArgumentException("Invalid choice");
                    };
                    List<Shape> sortedShapes = screen.getShapesSortedBy(comparator);
                    sortedShapes.forEach(shape -> System.out.println(shape.getShapeType() + " - " + shape.getArea()));
                }
                case 5 -> {
                    System.out.println("Enter point x and y:");
                    Point point = new Point(scanner.nextDouble(), scanner.nextDouble());
                    List<Shape> enclosingShapes = screen.getShapesEnclosingPoint(point);
                    enclosingShapes.forEach(shape -> System.out.println(shape.getShapeType() + " encloses the point."));
                }
                case 6 -> {
                    System.out.println("Enter base shape origin x and y:");
                    Point origin = new Point(scanner.nextDouble(), scanner.nextDouble());
                    Shape baseShape = screen.shapes.stream().filter(s -> s.getOrigin().equals(origin)).findFirst().orElse(null);
                    if (baseShape != null) {
                        List<Shape> shapesOnTop = screen.getShapesOnTopOf(baseShape);
                        shapesOnTop.forEach(shape -> System.out.println(shape.getShapeType() + " is on top."));
                    } else {
                        System.out.println("Base shape not found.");
                    }
                }
                default -> System.out.println("Invalid choice.");
            }
        }
        scanner.close();
    }
}