from PIL import Image
import time
start_time = time.time()
file_name = "maze_03"
im = Image.open(f"maze/{file_name}.png")
width, height = im.size
print(f"Picture size: {width}x{height}")
pixels = im.load()
mark = (255, 255, 255, 0)
white = (255, 255, 255, 255)
black = (0, 0, 0, 255)
green = (0, 255, 0, 255)

# region Find top left corner of a maze
leftBorder = 0
topBorder = 0
for i in range(0, width):
    if pixels[i, 1/2*height][0] < 255:
        leftBorder = i
        break
for i in range(0, height):
    if pixels[leftBorder, i][0] < 255:
        topBorder = i
        break
print(f"Top left corner detected: ({leftBorder}, {topBorder})")
# endregion

# region get tunnel size
leftTunnelWall = -1
rightTunnelWall = -1
for i in range(leftBorder, width):
    if pixels[i, topBorder] == white and leftTunnelWall == -1:
        print(f"left tunnel wall coordinates: ({i}, {topBorder})")
        leftTunnelWall = i-1
    elif pixels[i, topBorder] < white and leftTunnelWall >= 0 and rightTunnelWall == -1:
        print(f"right tunnel wall coordinates: ({i}, {topBorder})")
        rightTunnelWall = i

tunnel_size = rightTunnelWall - leftTunnelWall - 1
print(f"tunnel size: {tunnel_size}px")
# endregion

startingPoint = [leftBorder + 1, topBorder + 1]


class Solver:
    def __init__(self):
        self.currentPosition = startingPoint
        self.direction = 'South'

    def mark(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        pixels[x, y] = mark

    def draw(self):
        direction = self.direction
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        for i in range(0, tunnel_size-1):
            if direction == 'North':
                pixels[x - i, y] = green
            elif direction == 'East':
                pixels[x, y - i] = green
            elif direction == 'South':
                pixels[x + i, y] = green
            elif direction == 'West':
                pixels[x, y + i] = green

    def scan_for_walls(self):
        detector = [0, 0, 0, 0]
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        if pixels[x, y - 1][0] != 255:
            detector[0] = 1
        if pixels[x + 1, y][0] != 255:
            detector[1] = 1
        if pixels[x, y + 1][0] != 255:
            detector[2] = 1
        if pixels[x - 1, y][0] != 255:
            detector[3] = 1
        return detector

    def move(self, mark_or_draw):
        direction = self.direction
        print(f'direction: {direction}')
        if mark_or_draw == 'mark':
            self.mark()
        elif mark_or_draw == 'draw':
            self.draw()

        if direction == 'East':
            self.currentPosition[0] += 1
        elif direction == 'West':
            self.currentPosition[0] -= 1
        elif direction == 'South':
            self.currentPosition[1] += 1
        elif direction == 'North':
            self.currentPosition[1] -= 1

    def turn_right(self):
        previous_direction = self.direction
        if previous_direction == 'North':
            self.direction = 'East'
        elif previous_direction == 'East':
            self.direction = 'South'
        elif previous_direction == 'South':
            self.direction = 'West'
        elif previous_direction == 'West':
            self.direction = 'North'

    def turn_left(self):
        previous_direction = self.direction
        if previous_direction == 'North':
            self.direction = 'West'
        elif previous_direction == 'East':
            self.direction = 'North'
        elif previous_direction == 'South':
            self.direction = 'East'
        elif previous_direction == 'West':
            self.direction = 'South'

    def draw_the_route(self):
        self.currentPosition = [leftBorder + 1, topBorder + 1]
        count = 0
        self.direction = 'South'
        while self.currentPosition[1] < height - 10 and self.currentPosition[0] < width - 10:
            count += 1
            direction = self.direction
            if self.currentPosition[1] == height-2:
                self.currentPosition[1] -= 1
                self.turn_right()
                self.move('draw')
            x = self.currentPosition[0]
            y = self.currentPosition[1]
            surround_colors = {
                "North": pixels[x, y - 1],
                "East": pixels[x + 1, y],
                "South": pixels[x, y + 1],
                "West": pixels[x - 1, y]
            }
            # scan left side for shortcuts
            if surround_colors[direction] == mark:
                for i in range(1, tunnel_size):
                    if x+tunnel_size < width or y+tunnel_size < height:
                        if direction == 'North' and pixels[x - i, y] == mark:
                            self.turn_left()
                            self.move('draw')
                            break
                        elif direction == 'East' and pixels[x, y - i] == mark:
                            self.turn_left()
                            self.move('draw')
                            break
                        elif direction == 'South' and pixels[x + i, y] == mark:
                            self.turn_left()
                            self.move('draw')
                            break
                        elif direction == 'West' and pixels[x, y + i] == mark:
                            self.turn_left()
                            self.move('draw')
                            break
                        elif i == tunnel_size-1:
                            self.move('draw')
            elif surround_colors[direction] == white:
                for i in range(1, tunnel_size):
                    # if x+i >= width or y+i >= height:
                    #     self.move('draw')
                    #     break
                    if direction == 'North' and pixels[x, y - i] == mark:
                        self.move('draw')
                        break
                    elif direction == 'East' and pixels[x + i, y] == mark:
                        self.move('draw')
                        break
                    elif direction == 'South' and pixels[x, y + i] == mark:
                        self.move('draw')
                        break
                    elif direction == 'West' and pixels[x - i, y] == mark:
                        self.move('draw')
                        break
                    elif i == tunnel_size-1:
                        self.turn_right()
                        self.move('draw')
            elif surround_colors[direction] == black:
                self.turn_left()
                self.move('draw')
        print(f'result path length: {count} pixels')

    def find_the_way(self):
        count = 0
        while self.currentPosition[1] < height-1:
            count += 1
            walls_detected = self.scan_for_walls()
            print(f'walls {walls_detected}')
            if sum(walls_detected) == 0:
                self.turn_right()
                self.move('mark')
            elif sum(walls_detected) == 1:
                self.move('mark')
            elif sum(walls_detected) > 1:
                self.turn_left()
                self.move('mark')
        print(f'steps to find the exit: {count}')
        self.draw_the_route()


if __name__ == '__main__':

    solver = Solver()
    solver.find_the_way()

    im.save(f"solved/{file_name}_solved.png")
    print(f"total execution time: {round((time.time() - start_time)*1000, 3)}ms")
