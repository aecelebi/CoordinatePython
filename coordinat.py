from math import *
import enum


class SituationsForPointAndLine(enum.Enum):  # Noktanın doğruya göre durumları
    Below = 0,
    Above = 1,
    Contains = 2,


class CartesianRegions(enum.Enum):
    I = 1,
    II = 2,
    III = 3,
    IV = 4,
    Origin = 0,
    X_Axis = -1,
    Y_Axis = -2


class Point:  # Nokta sınıfını tanımlıyoruz
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.region = CartesianCoordinate.find_region(self)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.p1 = point1
        self.p2 = point2
        self.slope = CartesianCoordinate.calculate_slope_two(self.p1, self.p2)

    def __str__(self):
        pass


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = (p1, p2, p3)
        self.area = CartesianCoordinate.calculate_triangle_area(p1, p2, p3)


class CartesianCoordinate:  # Koordinat sistemi
    @staticmethod
    def calculate_angle(point1: Point, point2: Point, point3: Point):
        A = CartesianCoordinate.calculate_distance(point2, point3)
        B = CartesianCoordinate.calculate_distance(point1, point3)
        C = CartesianCoordinate.calculate_distance(point1, point2)

        cosC = (pow(A, 2) + pow(B, 2) - pow(C, 2)) / (2 * A * B)
        acosC = acos(cosC)

    @staticmethod
    def calculate_distance_to_origin(point: Point):
        origin = Point(0, 0)
        return sqrt(pow(abs(origin.x - point.x), 2) + pow(abs(origin.y - point.y), 2))

    @staticmethod
    def calculate_area(*args: Point):
        if len(args) < 3:
            return 0
        frame_points: [Point] = []
        lowest_point: Point
        highest_point: Point
        low_to_high = True

        lowest_point = args[0]
        highest_point = args[0]

        for i in args:
            if i.y < lowest_point.y:
                lowest_point = i
            if i.y > highest_point.y:
                highest_point = i  # Y değeri en yüksek ve en düşük noktayı seçiyoruz

        frame_points.append(lowest_point)
        # Y değeri en düşük noktayı kapsayacak bir nokta bulunmadığında çokgenin çevresinin bir parçasıdır

        while True:
            finish_loop = True

            for i in args:
                not_found = True
                for ix in args:
                    if not (CartesianCoordinate.check_is_point_in(i,
                                                                  frame_points) or (i.x == ix.x and i.y == i.y)):
                        result = CartesianCoordinate.check_point_situation_to_line(frame_points[-1], i, ix)
                        slope = CartesianCoordinate.calculate_slope_two(frame_points[-1], i)
                        # Çerçeveye eklenen son nokta ile noktalardan birini seçiyoruz(i)
                        # Sırayla(ix) diğer noktaların aralarında çektiğimiz doğruyla ilişkisini buluyoruz
                        print()
                        print(result)
                        print(slope)
                        print(low_to_high)
                        print(str(frame_points[-1]) + "  " + str(i) + "  " + str(ix))

                        if slope is None:
                            if not ((result == SituationsForPointAndLine.Above and low_to_high) or (
                                    result == SituationsForPointAndLine.Below and not low_to_high)):
                                not_found = False
                                break
                            # Eğer doğrumuz dikse ve nokta seçimlerimiz aşağıdan yukarıya ve doğru üstte kaldıysa ya da
                            # seçimlerimiz alta doğru ve doğru altta kaldıysa sorun yok demektir.
                            # Bunun aksi bir durum söz konusuysa i noktasını çerçeveye eklemiyoruz
                        elif slope == 0:
                            if (not low_to_high and SituationsForPointAndLine.Below) or (
                                    low_to_high and SituationsForPointAndLine.Above) and (i.y != highest_point.y):
                                not_found = False
                                break
                            # Benzer durum eğim 0 olduğunda geçerli
                        elif (result == SituationsForPointAndLine.Above and
                              ((not low_to_high and slope < 0) or
                               (low_to_high and slope > 0))) or \
                                (result == SituationsForPointAndLine.Below and
                                 ((not low_to_high and slope > 0) or
                                  (low_to_high and slope < 0))):
                            not_found = False
                            break
                            # Eğim varsa negatif ya da pozitif olma durumuna göre noktanın bulunduğu pozisyonun
                            # çokgenin çerçevesi için sorun oluşturup oluşturmadığına bakıyoruz

                if not_found and not CartesianCoordinate.check_is_point_in(i, frame_points):
                    finish_loop = False
                    frame_points.append(i)
                # Eğer i ve son çerçeve noktası arasında oluşturulan çizgiye göre tüm noktalar doğru yerdeyse i
                # bir sonraki çerçeve noktası demektir ve i'yi çerçeveye ekliyoruz.

                    if frame_points[-1].x == highest_point.x and frame_points[-1].y == highest_point.y:
                        low_to_high = False
                    # en yüksek noktaya geldiğimizde yönümüzü değiştiriyoruz
            if finish_loop:
                break
                # bunu hiçbir nokta kalmayana kadar yapıyoruz

        print(frame_points)

        for i in range(0, len(frame_points) - 1):
            if i != len(frame_points) - 2:
                if CartesianCoordinate.check_is_on_same_line(frame_points[i], frame_points[i + 1], frame_points[i + 2]):
                    frame_points.pop(i)
            else:
                if CartesianCoordinate.check_is_on_same_line(frame_points[0], frame_points[i], frame_points[i + 1]):
                    frame_points.pop(i + 1)
            # arka arkaya aynı doğruda olan 3 nokta olup olmadığını kontrol ediyoruz

        while True:
            changed = False
            for i in range(0, len(frame_points) - 1):
                if frame_points[i].y > frame_points[i + 1].y:
                    frame_points[i + 1], frame_points[i] = frame_points[i], frame_points[i + 1]
                    changed = True
                elif frame_points[i].y == frame_points[i + 1].y:
                    if (highest_point.x > lowest_point.x and frame_points[i].x > frame_points[i + 1].x) or (
                            highest_point.x < lowest_point.x and frame_points[i].x < frame_points[i + 1].x):
                        frame_points[i + 1], frame_points[i] = frame_points[i], frame_points[i + 1]
                        changed = True

            if not changed:
                break
            # noktaları y değerine göre küçükten büyüğe sıralıyoruz

        triangles: [(Point, Point, Point)] = []

        for i in range(0, len(frame_points) - 2):
            if CartesianCoordinate.check_point_situation_to_line(frame_points[i - 1], frame_points[i + 1], frame_points[
                i]) == SituationsForPointAndLine.Below and i != 0:
                triangles.append((frame_points[i - 1], frame_points[i + 1], frame_points[i + 2]))
            else:
                triangles.append((frame_points[i], frame_points[i + 1], frame_points[i + 2]))
            # çokgenimizi üçgenlere bölüyoruz. Ancak bu işlemi yaparken çakışma olmaması için üçer üçer seçtiğimiz
            # noktalardan şimdiki üçlünün ilk elemanının bir önceki üçlünün son elemanı ile sıradaki grubun 2.
            # elemanı arasında çizdiğimiz doğrunun altında kalıp kalmadığını kontrol ediyoruz
        print(frame_points)
        print(triangles)

        area = 0

        for i in triangles:
            area += CartesianCoordinate.calculate_triangle_area(i[0], i[1], i[2])
            #en sonda bu üçgenlerin alanını hesaplıyoruz ve topluyoruz
        return area

    @staticmethod
    def calculate_triangle_area(point1: Point, point2: Point, point3: Point) -> float:
        A = CartesianCoordinate.calculate_distance(point2, point3)
        B = CartesianCoordinate.calculate_distance(point1, point3)
        C = CartesianCoordinate.calculate_distance(point1, point2)

        cosC = (pow(A, 2) + pow(B, 2) - pow(C, 2)) / (2 * A * B) # Kosinüs teoreminden yararlanarak cos(BCA)'yı buluyoruz
        acosC = acos(cosC)
        sinC = sin(acosC)

        ABC = round(1 / 2 * A * B * sinC, 5) # Bu değeri sinüse çevirip Sinüs teoreminden yararlanıp alanı hesaplıyoruz
        print("\nA kenarı: " + str(A) + "\nB kenarı: " + str(B) + "\nC kenarı: " + str(C))

        print("cosC: " + str(cosC))
        print("acosC: " + str(acosC))
        print("sinC: " + str(sinC))
        print("Area of ABC: " + str(ABC) + "\n")

        return ABC


    @staticmethod
    def check_is_point_in(point_check: Point, points: [Point]):
        for i in points:
            if i.x == point_check.x and i.y == point_check.y:
                return True
        return False

    @staticmethod
    def check_is_on_same_line(point1: Point, point2: Point, point3: Point):
        if CartesianCoordinate.calculate_slope_two(point1, point2) == CartesianCoordinate.calculate_slope_two(point1,
                                                                                                              point3):
            return True
        else:
            return False

    @staticmethod
    def check_point_situation_to_line(point1: Point, point2: Point, point_to_check: Point) -> SituationsForPointAndLine:
        m = CartesianCoordinate.calculate_slope_two(point1, point2)

        if m != 0 and m is not None:
            c = point1.y - m * point1.x
            y_ref = m * point_to_check.x + c
        elif m is None:
            if point1.x == point_to_check.x:
                return SituationsForPointAndLine.Contains
            elif point1.x > point_to_check.x:
                return SituationsForPointAndLine.Below
            elif point1.x < point_to_check.x:
                return SituationsForPointAndLine.Above
        elif m == 0:
            if point1.y == point_to_check.y:
                return SituationsForPointAndLine.Contains
            elif point1.y > point_to_check.y:
                return SituationsForPointAndLine.Below
            elif point1.y < point_to_check.y:
                return SituationsForPointAndLine.Above

        if y_ref == point_to_check.y:
            return SituationsForPointAndLine.Contains
        elif y_ref > point_to_check.y:
            return SituationsForPointAndLine.Below
        elif y_ref < point_to_check.y:
            return SituationsForPointAndLine.Above

    @staticmethod
    def calculate_slope_two(point1, point2):
        try:
            return (point1.y - point2.y) / (point1.x - point2.x)
        except ZeroDivisionError:
            return None

    @staticmethod
    def calculate_distance(point1: Point, point2: Point):
        distance = sqrt(pow(abs(point1.x - point2.x), 2) + pow(abs(point1.y - point2.y), 2))
        return distance

    @staticmethod
    def center_point_between_two(point1: Point, point2: Point) -> Point:
        return Point((point1.x + point2.x) / 2, (point1.y + point2.y) / 2)

    @staticmethod
    def find_region(point: Point) -> CartesianRegions:
        if point.x > 0 and point.y > 0:
            return CartesianRegions.I
        elif point.x < 0 and point.y > 0:
            return CartesianRegions.II
        elif point.x < 0 and point.y < 0:
            return CartesianRegions.III
        elif point.x > 0 and point.y < 0:
            return CartesianRegions.IV
        elif point.x == 0 and not point.y == 0:
            return CartesianRegions.X_Axis
        elif point.y == 0 and not point.x == 0:
            return CartesianRegions.Y_Axis
        elif point.y == 0 and point.x == 0:
            return CartesianRegions.Origin


p1 = Point(0, 0)
p2 = Point(0, 1)
p4 = Point(2, 1)
p3 = Point(4, 8)
p5 = Point(4, 1)
p6 = Point(2, 3)
p7 = Point(3, 7)

print(CartesianCoordinate.calculate_area(p1, p4, p3, p2, Point(-3, -2), Point(-4, 8), Point(0, 10), Point(-6, 4)))
