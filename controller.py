class drawing_controller:
        '''drawing'''
        # if drawing menu is open or not
        draw_menu=0
        
        # if exit menu is open or not
        exit_menu=0
        
        # if images and labels have loaded or not
        on_drawing=0
        
        # 0,1,2
        brush=0
        
        # func on add glass/delete galss
        # 0 5 10
        brush_size=10
        
        def recover(self):
            self.draw_menu=0
            self.exit_menu=0
            self.on_drawing=0
            self.brush=0
            self.brush_size=10
            
            
            
            
class src_images:
    
    def __init__(self):
        self.bakimg=loadImage('./src/background.png')
        self.all_brush=[]
        self.brush_bk=loadImage('./src/menu_bk.png')
        self.exit_dialog=loadImage('./src/exit.png')
        self.loading_img=loadImage('./src/loading.png')
        self.all_brush.append(loadImage('./src/breakingbrush.png'))
        self.all_brush.append(loadImage('./src/tempbrush.png'))
        self.all_brush.append(loadImage('./src/colorbrush.png'))


class editting_controller:

    def __init__(self,img_idx,paths):
        self.image_label=[]
        self.image_edge=[]
        #brush 0 drawn
        self.drawed_label_0=[]
        # brush 1 drawn
        self.drawed_label_1=[]
        self.label2pix=[]
        image_label_txt=loadStrings("./data/lab_"+paths[img_idx][:-3]+"txt")
        
        for lines in image_label_txt:
            labels=list(map(int,lines.split(TAB)))
            # labels=lines.split(TAB)
            self.image_label.append(labels)
        max_label=int(self.image_label[-1][-1])
                
        image_edge_txt=loadStrings("./data/edge_"+paths[img_idx][:-3]+"txt")
        for lines in image_edge_txt:
            labels=lines.split(TAB)
            self.image_edge.append(labels)
            
            
        self.mosatic_img=loadImage("./data/mos_"+paths[img_idx][:-3]+"png")
        self.edit_img=loadImage('data/'+paths[img_idx])
        self.twinkle_label=[random(1) for i in range(max_label+1)]
        self.label2pix=[[] for i in range(max_label+1)]
        
        for x in range(height):
            for y in range(width):
                if (not self.image_label[x][y]==-1):
                    self.label2pix[int(self.image_label[x][y])].append([x,y])

        
       
