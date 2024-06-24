from sense_hat import SenseHat
import time
import datetime
import math

sense = SenseHat()

green = (0, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = [0, 0, 0]
yellow = [255, 215, 0]
pink = [255,0,127]
led_loop = [4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3]
currenttime_lapsed = 0
mins = 0
# Initialize step count and time
step_count = 0
last_step_time = time.time()

# Initialize timer variables
display_timer = 0
display_interval = 60  # 60 seconds (1 minute)

number = [
   # zero
   0, 1, 1, 1,
   0, 1, 0, 1,
   0, 1, 0, 1,
   0, 1, 1, 1,
   # one
   0, 0, 1, 0,
   0, 1, 1, 0,
   0, 0, 1, 0,
   0, 1, 1, 1,
   # two
   0, 1, 1, 1,
   0, 0, 0, 1,
   0, 0, 1, 0,
   0, 1, 1, 1,
   # three
   0, 1, 1, 1,
   0, 0, 0, 1,
   0, 0, 1, 1,
   0, 1, 1, 1,
   # four
   0, 1, 0, 1,
   0, 1, 0, 1,
   0, 1, 1, 1,
   0, 0, 0, 1,
   # five
   0, 1, 1, 1,
   0, 1, 0, 0,
   0, 0, 1, 1,
   0, 1, 1, 1,
   # six
   0, 1, 0, 0,
   0, 1, 1, 1,
   0, 1, 0, 1,
   0, 1, 1, 1,
   # seven
   0, 1, 1, 1,
   0, 0, 0, 1,
   0, 0, 1, 0,
   0, 1, 0, 0,
   # eight
   0, 1, 1, 1,
   0, 1, 1, 1,
   0, 1, 1, 1,
   0, 1, 1, 1,
   # nine
   0, 1, 1, 1,
   0, 1, 0, 1,
   0, 1, 1, 1,
   0, 0, 0, 1,
   #c
   0, 0, 0, 0,
   1, 1, 1, 0,
   1, 0, 0, 0,
   1, 1, 1, 0,
   
   #degrees
   1, 1, 0, 0,
   1, 1, 0, 0,
   0, 0, 0, 0,
   0, 0, 0, 0,
   
   #percentage
   1, 0, 0, 1,
   0, 0, 1, 0,
   0, 1, 0, 0,
   1, 0, 0, 1
]
  
def create_clock_image(hour, minute):
    clock_image = [0] * 64  # Initialize the clock image with all zeros

    # Pixel offset is used to navigate the number patterns
    pixel_offset = 0
    index = 0

    for index_loop in range(0, 4):
        for counter_loop in range(0, 4):
            if (hour >= 10):
                clock_image[index] = number[int(hour/10)*16 + pixel_offset]
            clock_image[index + 4] = number[int(hour % 10)*16 + pixel_offset]
            clock_image[index + 32] = number[int(minute/10)*16 + pixel_offset]
            clock_image[index + 36] = number[int(minute % 10)*16 + pixel_offset]
            pixel_offset = pixel_offset + 1
            index = index + 1
        index = index + 4

    for index in range(0, 64):
        if (clock_image[index]):
            if index < 32:
                clock_image[index] = pink
            else:
                clock_image[index] = white
        else:
            clock_image[index] = black

    return clock_image

# Function to display the clock image
def display_clock_image(clock_image):
    sense.set_pixels(clock_image)
    
def create_temp_image(temperature):
    temp_image = [0] * 64  # Initialize the clock image with all zeros

    # Pixel offset is used to navigate the number patterns
    pixel_offset = 0
    index = 0

    for index_loop in range(0, 4):
        for counter_loop in range(0, 4):
            if (temperature >= 10):
                temp_image[index] = number[int(temperature/10)*16 + pixel_offset]
            temp_image[index + 4] = number[int(temperature % 10)*16 + pixel_offset]
            temp_image[index + 32] = number[int(110/10)*16 + pixel_offset]
            temp_image[index + 36] = number[int(100/10)*16 + pixel_offset]
            #temp_image[index + 36] = number[int(temperature % 10)*16 + pixel_offset]
            pixel_offset = pixel_offset + 1
            index = index + 1
        index = index + 4

    for index in range(0, 64):
        if (temp_image[index]):
            if index < 32:
                if temperature >=30:
                    temp_image[index] = red
                else:
                    temp_image[index] = blue
            else:
                temp_image[index] = white
        else:
            temp_image[index] = black

    return temp_image

def display_temp_image(temp_image):
    sense.set_pixels(temp_image)
 
def create_humidity_image(humidity):
    humidity_image = [0] * 64  # Initialize the clock image with all zeros
    # Pixel offset is used to navigate the number patterns
    pixel_offset = 0
    index = 0

    for index_loop in range(0, 4):
        for counter_loop in range(0, 4):
            if (humidity >= 10):
                humidity_image[index] = number[int(humidity/10)*16 + pixel_offset]
            humidity_image[index + 4] = number[int(humidity % 10)*16 + pixel_offset]
            humidity_image[index + 34] = number[int(120/10)*16 + pixel_offset]
            pixel_offset = pixel_offset + 1
            index = index + 1
        index = index + 4


    for index in range(0, 64):
        if (humidity_image[index]):
            if index < 32:
                    humidity_image[index] = blue
            else:
                humidity_image[index] = white
        else:
            humidity_image[index] = black

    return humidity_image

def display_humidity_image(humidity_image):
    sense.set_pixels(humidity_image) 

def step_detection(acceleration):
    global step_count, last_step_time
    x, y, z = acceleration

    # Constants for step detection
    THRESHOLD = 1.0  # Adjust this threshold as needed
    MIN_STEP_TIME = 0.5  # Minimum time (in seconds) between steps

    # Calculate the magnitude of the acceleration vector
    acceleration_magnitude = math.sqrt(x**2 + y**2 + z**2)

    # Check if acceleration exceeds the threshold and enough time has passed
    current_time = time.time()
    if acceleration_magnitude > THRESHOLD and (current_time - last_step_time) > MIN_STEP_TIME:
        step_count += 1
        last_step_time = current_time
        
        
def create_step_image(step_count):
    step_image = [0] * 64  # Initialize the clock image with all zeros

    # Pixel offset is used to navigate the number patterns
    pixel_offset = 0
    index = 0

    for index_loop in range(0, 4):
        for counter_loop in range(0, 4):
            calorie_count = step_count * 0.4
            if (step_count >= 100):
                step_image[index] = number[int(step_count/10)*16 + pixel_offset]
            step_image[index + 4] = number[int(step_count % 10)*16 + pixel_offset]
            step_image[index + 32] = number[int(step_count/10)*16 + pixel_offset]
            pixel_offset = pixel_offset + 1
            index = index + 1
        index = index + 4

    for index in range(0, 64):
        if (step_image[index]):
            if index < 32:
                    step_image[index] = green
            else:
                step_image[index] = green
        else:
            step_image[index] = black

    return step_image

def display_step_image(step_image):
    sense.set_pixels(step_image)
    

def compass_app():
    prev_x = 0
    prev_y = 0
    led_degree_ratio = len(led_loop) / 360.0
    running = True      
    try:
            while running:
                heading = sense.get_compass()
                print(heading)
                for event in sense.stick.get_events():
                    if event.action == "pressed":
                        if event.direction == "down":
                            running = False
                if heading > 315 or heading < 45:
                    sense.show_letter('N', text_colour= blue, back_colour= black)
                elif heading > 45 and heading < 135:
                    sense.show_letter('E', text_colour= green, back_colour= black)
                elif heading > 135 and heading < 225:
                    sense.show_letter('S', text_colour= red, back_colour= black)
                elif heading > 225 and heading < 315:
                    sense.show_letter('W', text_colour= yellow, back_colour= black)
                
                dir_inverted = 90 - heading
                led_index = int(led_degree_ratio * dir_inverted)
                offset = led_loop[led_index]

                y = offset // 8  # row
                x = offset % 8  # column

                if x != prev_x or y != prev_y:
                    sense.set_pixel(prev_x, prev_y, 0, 0, 0)

                sense.set_pixel(x, y, 255, 0, 0)

                prev_x = x
                prev_y = y
                
    finally:
            sense.clear()
            time.sleep(0.5)
     

def create_timer_image(currenttime_lapsed):
    global mins
    timer_image = [0] * 64  # Initialize the clock image with all zeros
    if currenttime_lapsed == 60:
        mins += 1  
    # Pixel offset is used to navigate the number patterns
    pixel_offset = 0
    index = 0

    for index_loop in range(0, 4):
        for counter_loop in range(0, 4):
            timer_image[index] = number[int(mins/10)*16 + pixel_offset]
            timer_image[index + 4] = number[int(mins % 10)*16 + pixel_offset]
            timer_image[index + 32] = number[int(currenttime_lapsed/10)*16 + pixel_offset]
            timer_image[index + 36] = number[int(currenttime_lapsed % 10)*16 + pixel_offset]
            pixel_offset = pixel_offset + 1
            index = index + 1
        index = index + 4


    for index in range(0, 64):
        if (timer_image[index]):
            if index < 32:
                timer_image[index] = pink
            else:
                timer_image[index] = white
        else:
            timer_image[index] = black

    return timer_image

def display_timer_image(timer_image):
    sense.set_pixels(timer_image)
             
                             
def on_up_button_press():
    sense.clear()
    humidity = sense.humidity
    print(humidity)
    humidity_value = 64 * humidity / 100
    pixels = [green if i < humidity_value else white for i in range(64)]
    sense.set_pixels(pixels)
    time.sleep(2)
    sense.clear()

def on_down_button_press():
    running = True      
    try:
        while running:
            for event in sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "down":
                        running = False
                    if event.direction == "right":
                        while running:
                            humidity = sense.humidity
                            humidity_image = create_humidity_image(humidity)
                            display_humidity_image(humidity_image)
                            for event in sense.stick.get_events():
                                if event.action == "pressed":
                                    if event.direction == "down":
                                        running = False
            temperature = math.floor(sense.temp)
            temp_image = create_temp_image(temperature)
            display_temp_image(temp_image)
           
    finally:
        sense.clear()
        time.sleep(0.5)


def on_left_button_press():
    sense.clear()
    if step_count >=100:
        sense.show_message(f"Steps: {step_count}", scroll_speed=0.05, text_colour=[0, 255, 0], back_colour=[0, 0, 0])
        time.sleep(2)
        sense.clear()
    else:
        step_image= create_step_image(step_count)
        display_step_image(step_image)
        print(step_count)
        time.sleep(2)
        sense.clear()
        
def on_right_button_press():
    compass_app()

def on_middle_button_press():
    sense.clear()
    
    print("lol")
    running = True      
    try:
        while running:
            for event in sense.stick.get_events():
                    if event.action == "pressed":
                        if event.direction == "up":
                            start_time = time.time()
                            while running:
                                   global currenttime_lapsed
                                   currenttime_lapsed = math.floor(time.time()-start_time)
                                   if currenttime_lapsed == 60:
                                        start_time = time.time()
                                        
                                   timer_image=create_timer_image(currenttime_lapsed)
                                   display_timer_image(timer_image)
                                   time.sleep(1)
                                   
                                   for event in sense.stick.get_events():
                                       if event.action == "pressed":                                               
                                        if event.direction == "down":
                                            currenttime_lapsed = math.floor(time.time()-start_time)
                                            timer_image=create_timer_image(currenttime_lapsed)
                                            display_timer_image(timer_image)
                                            time.sleep(1)
                                            running = False                  
    finally:
        sense.clear()

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    step_detection((x, y, z))
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min

    # Create the clock image using the function
    clock_image = create_clock_image(hour, minute)

    # Display the clock image using the function
    display_clock_image(clock_image)

    time.sleep(1) 

    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "up":
                on_up_button_press()
            elif event.direction == "down":
                on_down_button_press()
            elif event.direction == "left":
                on_left_button_press()
            elif event.direction == "right":
                on_right_button_press()
            elif event.direction == "middle":
                on_middle_button_press()
                
                
















