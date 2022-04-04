#######################################################################
##                                                                   ##
##                                                                   ##
##  Ethan Coyle                                                      ##
##  Dr. Griffin - CMPS 4551 Spatial Data Structures                  ##
##  P07 - pygame moving rectangle with collision detection           ##
##                                                                   ##
#######################################################################
##                                                                   ##
##  The purpose of this assignment is to create a pygame             ##
##  application that will allow the user to draw a                   ##
##  rectangle and then have the program randomly generate            ##
##  a number of points within the rectangle. The program             ##
##  will then draw the points as blue circles and the                ##
##  rectangle as a red rectangle. The user will be able              ##
##  to move the rectangle around the screen and the                  ##
##  program will detect if the rectangle is colliding                ##
##  with any of the points.                                          ##
##                                                                   ##
## User notes: this game works in replit using a pygame.py           ##
## file.                                                             ##
## so i am attaching my pygame file to this file.                    ##
##                                                                   ##
## Link to working game :                                            ##
# https://replit.com/@ethancoyle71/WebbedSlategreyParameters#main.py ##
##                                                                   ##
##                                                                   ##
#######################################################################
# create the imports for the game
import pygame, sys, random


# define the pygame main window size.
MAIN_WINDOW_SIZE = (250,250)
# this function will return a tuple with random x, y integer value.
def RandomPoints(max_x ,max_y):
    # set at a rnd x and y point 
    point_x = random.randint(0, max_x)
    point_y = random.randint(0, max_y)
    # return that random spot
    return (point_x, point_y)
     
def RectangleCollision():
    
    # initialize pygame application.
    pygame.init()
    # create the pygame surface object
    main_window_screen = pygame.display.set_mode(MAIN_WINDOW_SIZE)
    # now we need to set a title to display at the top of the screen
    pygame.display.set_caption('Pygame and Point Collision.')
    
    # creating stuff for our rectangle
    # rectagle top left coordinates
    Rectangle_left = 0  # x  
    Rectangle_top = 0   # y
    Rectangle_width = 100 # width
    Rectangle_height = 100 # height
    # create the pygame.Rect object with the above values.
    # initialize our rectangle
    Rectangle = pygame.Rect(Rectangle_left, Rectangle_top, Rectangle_width, Rectangle_height)
    
   
    
    
    # declare the point list to save all random generated points coordinates.
    ListOfPoints = []
    # We arer going to generate 100 random points.
    NumPoints = 100
    for i in range(NumPoints):
        # create a point with random coordinate values.
        TempPoints = RandomPoints(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])
        # add the point to the list.
        ListOfPoints.append(TempPoints) # append them to our points list
                                     # held within out window size we 
                                     # initialized earlier.    
    # now we need to draw the rectangle and the points.
    # Main loop while true.
    while True:
        # fill the main window background color to gray.
        main_window_screen.fill(pygame.Color('gray'))
        # draw the big red Rectangleangle on the main window screen. 
        pygame.draw.rect(main_window_screen, pygame.Color('red'), Rectangle, 2)
        
        # # process events.
        for event in pygame.event.get():
            # for exitting the game
            if event.type == pygame.QUIT:# if the user clicks the X button
                pygame.quit()# quit the game
                sys.exit(0)# exit the program
        # define the point circle radius.
        point_radius = 6
        # draw each point in the ListOfPoints.
        for point in ListOfPoints:
            # if the big red Rectangleangle collides the point.
            # the dots inside the rectangle will be drawn as green color
            if Rectangle.collidepoint(point):
                # create a random color for the point.
                point_color = pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                # draw the point as a circle.
                pygame.draw.circle(main_window_screen, point_color, point, point_radius,0)

                # pygame.draw.circle(main_window_screen, pygame.Color('green'), point, point_radius, 0)   
            else:
                # if the rectangle isnt hovering over the circles, then draw them as blue color.
                pygame.draw.circle(main_window_screen, pygame.Color('blue'), point, point_radius, 0)   
        # update the main window screen.

       
       # move the rectangle to the right and when it is out of the screen,
       #  move it down and then back to the left
        Rectangle.move_ip(2,0)
        if Rectangle.right > MAIN_WINDOW_SIZE[0]:
            Rectangle.move_ip(-MAIN_WINDOW_SIZE[0],100)
        # once this is done, repeat the loop.
        pygame.display.update()
        # set the frame rate to 60 frames per second.
        pygame.time.Clock().tick(60)
        # if the rectangle is out of the screen on the bottom right, 
        # return it to the top left and continue the loop.
        if Rectangle.bottom > MAIN_WINDOW_SIZE[1]:
            Rectangle.move_ip(-MAIN_WINDOW_SIZE[0],-MAIN_WINDOW_SIZE[1])
        # # update the main window screen.
        pygame.display.update()
        # # set the main window screen to 60 fps.
        pygame.time.delay(60)
        
        pygame.display.flip()      
# main driver draw the recttangle and the circles to be used with the mouse.
if __name__ == '__main__':
    # go to the function definition, and draw the screen items.
    RectangleCollision()# call the function
    # if the user clicks the X button, quit the game.
