'''
Zhang Fan. 
Digital Media Tech. JNU China
'''
from controller import drawing_controller
from controller import src_images
from controller import editting_controller
import copy
def setup():
    '''
    [current state]
    0:on setup
    1:on STATIC menu
    2:on MOVING menu 
    3:menu to draw
    4:prepare to draw
    5:on draw
    6:draw to menu
    '''
    global stat
    stat = 0
    
    # which picture user select
    global picture_idx
    picture_idx = -1
    
    '''on moving menu:'''
    global picture_idx_bak
    picture_idx_bak = -1
    
    global move_menu
    move_menu=0
    
    '''menu to draw'''
    global img_unfold
    img_unfold=760
    
    '''costom's image. images should be put in ./data
    the file name added in path.txt'''
    global paths
    paths = loadStrings("path.txt")
    
    global draw_control 
    draw_control=drawing_controller()
    
    global src_img
    src_img=src_images()
    
    # costom's image set
    global img_list
    img_list=[loadImage('data/'+i) for i in paths]

    # window
    size(960, 720)
    
    global twinkle_rate
    twinkle_rate=0

def draw():
    global stat
    global picture_idx
    
    background(src_img.bakimg)
    if(stat == 0):
        # initlization
        stat = 1
        picture_idx = 0
        show_img = img_list[picture_idx]
        image(show_img, 960/2-380,720/2-285, 760, 570)
    elif(stat == 1):
        #show pictures
        show_img = img_list[picture_idx]
        image(show_img, 960/2-380,720/2-285, 760, 570)
        
        if mousePressed:
            #swich pictures
            if(0<mouseX<100 and picture_idx>0):
                global picture_idx_bak
                picture_idx_bak=picture_idx
                picture_idx -=1
                stat=2
            
            elif(860<mouseX<960 and picture_idx<len(img_list)-2):
                global picture_idx_bak
                picture_idx_bak=picture_idx
                picture_idx +=1
                stat=2
            elif(960/2-240<mouseX<960/2+240):
                stat=3
                
        
    elif(stat == 2):
        global picture_idx_bak
        global move_menu
        
        pushMatrix()
        translate(move_menu,0)
        
        show_img1 = img_list[picture_idx_bak]
        img_scale1=float(show_img1.height)/show_img1.width
        image(show_img1, 960/2-380,720/2-285, 760, 570)
        if(picture_idx_bak<picture_idx):
            show_img2 = img_list[picture_idx]
            img_scale2=float(show_img2.height)/show_img2.width
            image(show_img2, 960/2-380+960,720/2-285, 760, 570)
            
            popMatrix()
            move_menu-=30
            if(move_menu<-960):
                stat=1
                move_menu=0
        else:
            show_img2 = img_list[picture_idx]
            img_scale2=float(show_img2.height)/show_img2.width
            image(show_img2, 960/2-380-960,720/2-285, 760, 570)
            
            popMatrix()
            move_menu+=30
            if(move_menu>960):
                stat=1
                move_menu=0
    elif(stat==3):
        global img_unfold
        show_img = img_list[picture_idx]
        img_scale=float(show_img.height)/show_img.width
        image(show_img, 960/2-img_unfold/2,720/2-img_unfold/2*img_scale, img_unfold, img_unfold*img_scale)
        img_unfold+=15
        if(img_unfold>960):
            image(src_img.loading_img,330,260)
            stat=4
    elif(stat==4):
        show_img = img_list[picture_idx]
        image(show_img, 0,0)
        image(src_img.loading_img,330,260)
        
        global edit_contrl
        edit_contrl=editting_controller(picture_idx,paths)
        # print(picture_idx)
            
        stat=5
        
    elif(stat==5):
        global draw_control
        
        if(draw_control.on_drawing==0):
            draw_control.on_drawing=1
            show_img = img_list[picture_idx]
            image(show_img, 0,0)
            
        image(edit_contrl.edit_img,0,0)
        twinkle_glass()
        if(draw_control.draw_menu==0 and draw_control.exit_menu==0):
            if mousePressed:
                # MAIN: invert image to mosatic image
                update_image()
                twinkle_glass() 
                # should be update as soon as some label delete from image
                
            fill(255,100)
            ellipse(mouseX,mouseY,draw_control.brush_size,draw_control.brush_size)
        elif(draw_control.draw_menu==1):
            # draw menu background
            tint(255,255,255,150)
            image(src_img.brush_bk,75,650)
            image(src_img.brush_bk,575,650)
            tint(255)
            
            # draw brushs
            image(src_img.all_brush[draw_control.brush],100*(draw_control.brush+1),650)
            other_brush=[0,1,2]
            del other_brush[draw_control.brush]
            for i in other_brush:
                image(src_img.all_brush[i],100*(i+1),670)
            
            #draw brush size
            
            if(draw_control.brush_size==10):
                fill(255, 255)
                ellipse(630,690,10,10)
                fill(255, 100)
                ellipse(700,690,30,30)
                ellipse(790,690,50,50)
            elif(draw_control.brush_size==30):
                fill(255, 255)
                ellipse(700,690,30,30)
                fill(255, 100)
                ellipse(630,690,10,10)
                ellipse(790,690,50,50)
            else:
                fill(255, 255)
                ellipse(790,690,50,50)
                fill(255, 100)
                ellipse(630,690,10,10)
                ellipse(700,690,30,30)
                
            if mousePressed:
                if(mouseY<600):
                    draw_control.draw_menu=0
                elif(100<mouseX<200):
                    draw_control.brush=0
                elif(200<mouseX<300):
                    draw_control.brush=1
                elif(300<mouseX<400):
                    draw_control.brush=2
                elif(620<mouseX<640):
                    draw_control.brush_size=10
                elif(680<mouseX<720):
                    draw_control.brush_size=30
                elif(740<mouseX<840):
                    draw_control.brush_size=50

        elif(draw_control.draw_menu==0 and draw_control.exit_menu==1):
            image(src_img.exit_dialog,330,260)
            
            if mousePressed:
                global edit_contrl
                if(330<mouseX<480 and 360<mouseY<460):
                    draw_control.recover()
                    image(edit_contrl.edit_img,0,0)
                    save("./gallery/"+str(hour())+'_'+str(minute())+'_'+str(second())+".png")
                    stat=6
                    del edit_contrl
                elif(480<mouseX<630 and 360<mouseY<460):
                    draw_control.recover()
                    stat=6
                    del edit_contrl
        
        
    
    elif(stat==6):
        global img_unfold
        show_img = img_list[picture_idx]
        img_scale=float(show_img.height)/show_img.width
        image(show_img, 960/2-img_unfold/2,720/2-img_unfold/2*img_scale, img_unfold, img_unfold*img_scale)
        img_unfold-=15
        if(img_unfold<760):
            stat=1
       
            
        
def keyPressed():
    global stat
    global draw_control
    if (stat==5 and ord(key)==ord(' ') and draw_control.draw_menu==0):
        draw_control.draw_menu=1
    elif (stat==5 and ord(key)==ord(' ') and draw_control.draw_menu==1):
        draw_control.draw_menu=0
        image(edit_contrl.edit_img,0,0)
    elif (stat==5 and key=='e'):
        draw_control.draw_menu=0
        draw_control.exit_menu=1
        
        
        
def update_image():
    global edit_contrl
    
    
    # add glass 0
    if draw_control.brush==0:
        
        if draw_control.brush_size==10:
            try:
                current_label=edit_contrl.image_label[mouseY][mouseX]
            except:
                pass
            else:
                if (len(edit_contrl.drawed_label_0)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_0.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
                        
        elif draw_control.brush_size==30:
            current_label_list=[]
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15]]:
                try:
                    current_label_list.append(edit_contrl.image_label[mouseY+sx][mouseX+sy])
                except:
                    pass
            for current_label in current_label_list:
                if (len(edit_contrl.drawed_label_0)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_0.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
                        
        elif draw_control.brush_size==50:
            current_label_list=[]
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15],[-25,-25],[25,25],[25,-25],[-25,25]]:
                try:
                    current_label_list.append(edit_contrl.image_label[mouseY+sx][mouseX+sy])
                except:
                    pass
            for current_label in current_label_list:
                if (len(edit_contrl.drawed_label_0)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_0.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
            
    # add glass 1
    if draw_control.brush==1:
        
        if draw_control.brush_size==10:
            try:
                current_label=edit_contrl.image_label[mouseY][mouseX]
            except:
                pass
            else:
                if(len(edit_contrl.drawed_label_1)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_1.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
                        
        elif draw_control.brush_size==30:
            current_label_list=[]
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15]]:
                try:
                    current_label_list.append(edit_contrl.image_label[mouseY+sx][mouseX+sy])
                except:
                    pass
            for current_label in current_label_list:
                if (len(edit_contrl.drawed_label_1)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_1.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
                        
        elif draw_control.brush_size==50:
            current_label_list=[]
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15],[-25,-25],[25,25],[25,-25],[-25,25]]:
                try:
                    current_label_list.append(edit_contrl.image_label[mouseY+sx][mouseX+sy])
                except:
                    pass
            for current_label in current_label_list:
                if (len(edit_contrl.drawed_label_1)==0 or (not current_label in edit_contrl.drawed_label_0) or (not current_label in edit_contrl.drawed_label_1)):
                    edit_contrl.drawed_label_1.append(current_label)
                for pos in edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=edit_contrl.mosatic_img.get(y,x)
                            
    # delete glass              
    elif draw_control.brush==2:
        if draw_control.brush_size==10:
            try:
                current_label=edit_contrl.image_label[mouseY][mouseX]
                edit_contrl.drawed_label_0.remove(current_label)
            except:
                try:
                    edit_contrl.drawed_label_1.remove(current_label)
                except:
                    pass
                else:
                    for pos in  edit_contrl.label2pix[current_label]:
                        x=pos[0]
                        y=pos[1]
                        if(edit_contrl.image_label[x][y]==current_label):
                            edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)        
            else:
                for pos in  edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    # if(edit_contrl.image_label[x][y]==current_label):
                    edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)
        if draw_control.brush_size==30:
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15]]:
                try:
                    current_label=edit_contrl.image_label[mouseY+sx][mouseX+sy]
                    edit_contrl.drawed_label_0.remove(current_label)
                except:
                    try:
                        edit_contrl.drawed_label_1.remove(current_label)
                    except:
                        pass
                    else:
                        for pos in  edit_contrl.label2pix[current_label]:
                            x=pos[0]
                            y=pos[1]
                            if(edit_contrl.image_label[x][y]==current_label):
                                edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)        
            else:
                for pos in  edit_contrl.label2pix[current_label]:
                    x=pos[0]
                    y=pos[1]
                    # if(edit_contrl.image_label[x][y]==current_label):
                    edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)
        if draw_control.brush_size==50:
            for sx,sy in [[0,0],[-15,0],[15,0],[0,-15],[0,15],[-25,-25],[25,25],[25,-25],[-25,25]]:
                try:
                    current_label=edit_contrl.image_label[mouseY+sx][mouseX+sy]
                    edit_contrl.drawed_label_0.remove(current_label)
                except:
                    try:
                        edit_contrl.drawed_label_1.remove(current_label)
                    except:
                        pass
                    else:
                        for pos in  edit_contrl.label2pix[current_label]:
                            x=pos[0]
                            y=pos[1]
                            if(edit_contrl.image_label[x][y]==current_label):
                                edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)        
                else:
                    for pos in  edit_contrl.label2pix[current_label]:
                        x=pos[0]
                        y=pos[1]
                        # if(edit_contrl.image_label[x][y]==current_label):
                        edit_contrl.edit_img.pixels[x*width+y]=img_list[picture_idx].get(y,x)

                
# twinkle_glass()
    edit_contrl.edit_img.updatePixels()
    
    
def twinkle_glass():
    global edit_contrl
    global twinkle_rate
    for labels in edit_contrl.drawed_label_1:
        pos=edit_contrl.label2pix[labels][10]
        while(edit_contrl.image_edge[pos[0]][pos[1]]=='1'):
            pos=edit_contrl.label2pix[labels][int(random(len(edit_contrl.label2pix[labels])))]
        temp_color=edit_contrl.mosatic_img.get(pos[1],pos[0])
        temp_bate=1+sin(twinkle_rate+edit_contrl.twinkle_label[labels]*2*PI)/2.0
        temp_r=red(temp_color)*temp_bate
        temp_g=green(temp_color)*temp_bate
        temp_b=blue(temp_color)*temp_bate
        for pos in edit_contrl.label2pix[labels]:
            x=pos[0]
            y=pos[1]
            # print(edit_contrl.image_edge[x][y])
            if edit_contrl.image_edge[x][y]=='0':
                # print (temp_r)
                twinkle_color=color(temp_r,temp_g,temp_b)
                edit_contrl.edit_img.pixels[x*width+y]=twinkle_color
    edit_contrl.edit_img.updatePixels()
    image(edit_contrl.edit_img,0,0)
    twinkle_rate=twinkle_rate+0.05
    
