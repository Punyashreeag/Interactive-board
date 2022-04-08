#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
import os

global canvas
# canvas and tooolbar creation
canvas=np.zeros((700,800,3),np.uint8)
canvas_hidden=np.zeros((700,800,3),np.uint8)
canvas[:,:]=(255,255,255)

toolbar=np.zeros((47,800,3),np.uint8)
cv2.line(toolbar,(200,0),(200,47),(255,255,255),3)
cv2.line(toolbar,(400,0),(400,47),(255,255,255),3)
cv2.line(toolbar,(600,0),(600,47),(255,255,255),3)

cv2.putText(toolbar,'+image',(10,30), 3, 1,(255,255,255),2,0)
cv2.putText(toolbar,'+text',(210,30), 3, 1,(255,255,255),2,0)
cv2.putText(toolbar,'ink',(410,30), 3, 1,(255,255,255),2,0)
cv2.putText(toolbar,'new',(610,30), 3, 1,(255,255,255),2,0)
canvas[0:47,:]=toolbar

#setting up gallery
gallery=np.zeros((700,600,3),np.uint8)
gallery[:,:]=(255,255,255)
path='D:\B\INTERACTIVE BOARD\images'
store_path='D:\B\INTERACTIVE BOARD\saved_images'
global page_no
global img_index
global new_canvas
global img_count
img_count=1
new_canvas=-1
img_index=-1
page_no=1
previous=np.zeros((50,100,3),np.uint8)
previous[:,:]=(100,100,100)
nex=np.zeros((50,100,3),np.uint8)
nex[:,:]=(100,100,100)
gallerylist= os.listdir(path)
cv2.putText(previous,'prev',(10,30), 3, 1,(255,255,255),2,0)
cv2.putText(nex,'next',(10,30), 3, 1,(255,255,255),2,0)

global head
head=1

global vertices_list
global img_list
global ink
global image
global index
global operation
global reloc_x
global reloc_y
global write
global ink_enable
img_list=[]
vertices_list=[]



write=-1
ink,image,index,operation,reloc_x,reloc_y=-1,0,-1,-1,-1,-1
ink_enable=-1
def selection(event,x,y,flags,param):
    global image
    global ink
    global index
    global operation
    global vertices_list
    global img_list
    global reloc_x
    global reloc_y
    global new_canvas
    
    index=-1
    operation=-1
    if event==cv2.EVENT_LBUTTONDBLCLK:
        
        if(x<=200 and y<=47):
            print("image insertion")
            image=1
        elif(x>400 and x<=600 and y<=47):
            print('ink selection')
            ink=1
        elif(x>600 and x<=800 and y<=47):
            print('new_canvas')
            new_canvas=1
       
        else:
            
            
           
            for (num,vertices) in enumerate(vertices_list):
                #resize from top left corner
                if((x>=vertices[0][0]-10 and x<=vertices[0][0]+10) and (y>vertices[0][1]-10 and y<vertices[0][1]+10)):
                    index=num
                    operation=1
                #resize from top right corner
                elif((x>=vertices[1][0]-10 and x<=vertices[1][0]+10) and (y>vertices[1][1]-10 and y<vertices[1][1]+10)):
                    index=num
                    operation=2
                #resize from bottom left corner
                elif((x>=vertices[1][0]-10 and x<=vertices[1][0]+10) and (y>vertices[1][1]-10 and y<vertices[1][1]+10)):
                    index=num
                    operation=2
                #resize from bottom right corner
                elif((x>=vertices[2][0]-10 and x<=vertices[2][0]+10) and (y>vertices[2][1]-10 and y<vertices[2][1]+10)):
                    index=num
                    operation=3
                # image movement
                elif((x>=vertices[3][0]-10 and x<=vertices[3][0]+10) and (y>vertices[3][1]-10 and y<vertices[3][1]+10)):
                    
                    index=num
                    operation=4
                elif((x>=vertices[0][0]+10 and x<=vertices[3][0]-10) and (y>vertices[0][1]+10 and y<vertices[3][1]-10)):
                    index=num
                    operation=5
                    reloc_x=x
                    reloc_y=y
                    print('reloc_x:',reloc_x)
                    print('reloc_y:',reloc_y)
                    
            print(index)
            print(operation)
            if(index!=-1 and operation!=-1):
                tl=vertices_list[index][0]
                tr=vertices_list[index][1]
                bl=vertices_list[index][2]
                br=vertices_list[index][3]
                temp_img=img_list[index]
                img_list.pop(index)
                img_list.append(temp_img)
                vertices_list.pop(index)
                temp_list=[tl,tr,bl,br]
                vertices_list.append(temp_list)
                index=len(img_list)-1
           
                    
def add_image(img):
    global image
    img=cv2.resize(img,(300,300))
    canvas[50:50+img.shape[0],1:img.shape[1]+1]=img
    img_list.append(img)
    vertices=[]
    tl=[1,50]
    tr=[1+img.shape[1],50]
    bl=[1,img.shape[0]+50]
    br=[img.shape[1]+1,img.shape[0]+50]
    vertices=[tl,tr,bl,br]
    vertices_list.append(vertices)
    print(len(img_list))
    print(vertices_list)
    cv2.destroyWindow('gallery')
    image=0
    
def perform_operations(event,x,y,flags,param):
    global index
    global operation
    global canvas
    global vertices_list
    global img_list
    
    if operation==1:
        
        if event==cv2.EVENT_LBUTTONDBLCLK:
            print('aaaaaa')
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            
            j=cv2.resize(img_list[index],(vertices_list[index][3][0]-x,vertices_list[index][3][1]-y))
            
            canvas[y:vertices_list[index][3][1],x:vertices_list[index][3][0]]=j
            
            vertices_list[index][0]=[x,y]
            vertices_list[index][2][0]=x
            vertices_list[index][1][1]=y
            
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
            operation=-1
            index=-1
        if event==cv2.EVENT_MOUSEMOVE:
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            j=cv2.resize(img_list[index],(vertices_list[index][3][0]-x,vertices_list[index][3][1]-y))
            
            canvas[y:vertices_list[index][3][1],x:vertices_list[index][3][0]]=j
            
            vertices_list[index][0]=[x,y]
            vertices_list[index][2][0]=x
            vertices_list[index][1][1]=y
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
    if operation==2:
        
        if event==cv2.EVENT_LBUTTONDBLCLK:
            
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            
            j=cv2.resize(img_list[index],(x-vertices_list[index][2][0],vertices_list[index][2][1]-y))
            
            canvas[y:vertices_list[index][2][1],vertices_list[index][2][0]:x]=j
            
            vertices_list[index][1]=[x,y]
            vertices_list[index][3][0]=x
            vertices_list[index][0][1]=y
            
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
            operation=-1
            index=-1
        if event==cv2.EVENT_MOUSEMOVE:
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            j=cv2.resize(img_list[index],(x-vertices_list[index][2][0],vertices_list[index][2][1]-y))
            
            canvas[y:vertices_list[index][2][1],vertices_list[index][2][0]:x]=j
            
            vertices_list[index][1]=[x,y]
            vertices_list[index][3][0]=x
            vertices_list[index][0][1]=y
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
    if operation==3:
        
        if event==cv2.EVENT_LBUTTONDBLCLK:
            
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            
            j=cv2.resize(img_list[index],(vertices_list[index][1][0]-x,y-vertices_list[index][1][1]))
            
            canvas[vertices_list[index][1][1]:y,x:vertices_list[index][1][0]]=j
            
            vertices_list[index][2]=[x,y]
            vertices_list[index][0][0]=x
            vertices_list[index][3][1]=y
            
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
            operation=-1
            index=-1
        if event==cv2.EVENT_MOUSEMOVE:
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            j=cv2.resize(img_list[index],(vertices_list[index][1][0]-x,y-vertices_list[index][1][1]))
            
            canvas[vertices_list[index][1][1]:y,x:vertices_list[index][1][0]]=j
            
            vertices_list[index][2]=[x,y]
            vertices_list[index][0][0]=x
            vertices_list[index][3][1]=y
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
    if operation==4:
        
        if event==cv2.EVENT_LBUTTONDBLCLK:
            
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            
            j=cv2.resize(img_list[index],(x-vertices_list[index][0][0],y-vertices_list[index][0][1]))
            
            canvas[vertices_list[index][0][1]:y,vertices_list[index][0][0]:x]=j
            
            vertices_list[index][3]=[x,y]
            vertices_list[index][1][0]=x
            vertices_list[index][2][1]=y
            
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
            operation=-1
            index=-1
        if event==cv2.EVENT_MOUSEMOVE:
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            
            j=cv2.resize(img_list[index],(x-vertices_list[index][0][0],y-vertices_list[index][0][1]))
            
            canvas[vertices_list[index][0][1]:y,vertices_list[index][0][0]:x]=j
            
            vertices_list[index][3]=[x,y]
            vertices_list[index][1][0]=x
            vertices_list[index][2][1]=y
            

            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j

    if operation==5:
        global reloc_x
        global reloc_y
        if event==cv2.EVENT_LBUTTONDBLCLK:
            print('x:',x)
            print('y:',y)
            print('reloc_x:',reloc_x)
            print('reloc_y:',reloc_y)
            x_diff=x-reloc_x
            y_diff=y-reloc_y
            print('x_diff',x_diff)
            print('y_diff',y_diff)
        
            canvas[vertices_list[index][0][1]-3:vertices_list[index][3][1]+3,vertices_list[index][0][0]-1:vertices_list[index][1][0]+3]=255
            j=cv2.resize(img_list[index],(vertices_list[index][3][0]-vertices_list[index][0][0],vertices_list[index][3][1]-vertices_list[index][0][1]))
        
            canvas[vertices_list[index][0][1]+y_diff:vertices_list[index][3][1]+y_diff,vertices_list[index][0][0]+x_diff:vertices_list[index][3][0]+x_diff]=j
        
            vertices_list[index][0][0]+=x_diff
            vertices_list[index][1][0]+=x_diff
            vertices_list[index][2][0]+=x_diff
            vertices_list[index][3][0]+=x_diff
        
            vertices_list[index][0][1]+=y_diff
            vertices_list[index][1][1]+=y_diff
            vertices_list[index][2][1]+=y_diff
            vertices_list[index][3][1]+=y_diff
        
            for (vertices,images) in zip(vertices_list,img_list) :
                j=cv2.resize(images,(vertices[3][0]-vertices[0][0],vertices[3][1]-vertices[0][1]))
                canvas[vertices[0][1]:vertices[3][1],vertices[0][0]:vertices[3][0]]=j
            operation=-1
            index=-1

def ink_pen(event,x,y,flags,param): 

    
    global write
    global ink
   
    

    if event==cv2.EVENT_FLAG_LBUTTON:
        write=0-write
        
    if write==1:
        if event==cv2.EVENT_MOUSEMOVE:
            cv2.circle(canvas,(x,y),3,(0,0,255),-1)
    if (ink==1 and write==1):
        if event==cv2.EVENT_LBUTTONDBLCLK:
            ink=-1
            
            
def page_selection(event,x,y,flags,param):
        
    global page_no
    global img_index
    if event==cv2.EVENT_LBUTTONDBLCLK:
        
        if page_no!=1 and (x<=275 and x>=175) and(y>=50 and y<=100):
                page_no-=1
                
        elif (page_no*9<len(gallerylist)) and  (x<=425 and x>=325) and(y>=50 and y<=100):
                page_no+=1
                
        for index in range(0,9):
            r=index//3
            col=index%3
            if((x>=(50*(col+1))+150*col and x<=(50*(col+1))+150*col+150) and (y>=100+(50*(r+1))+150*r and y<=100+(50*(r+1))+150*r+150)):
                img_index=9*(page_no-1)+index
        if img_index!=-1:
            images=gallerylist[img_index]
            cur_img=cv2.imread(f'{path}/{images}')
            add_image(cur_img)
                
def set_page():
    global page_no
    gallery[50:100,:]=(255,255,255)
    if (page_no*9)<len(gallerylist):
        gallery[50:100,325:425]=nex
    if page_no!=1:
        gallery[50:100,175:275]=previous
        
    for index in range(0,9):
        r=index//3
        col=index%3
        loc_x=(50*(col+1))+150*col
        loc_y=100+(50*(r+1))+150*r
        if(9*(page_no-1)+index>=len(gallerylist)):
            break
        else:
        
            images=gallerylist[9*(page_no-1)+index]
            curimg=cv2.imread(f'{path}/{images}')
            curimg=cv2.resize(curimg,(150,150))
            gallery[loc_y:loc_y+150,loc_x:loc_x+150]=curimg

    
def save_canvas():
    global vertices_list
    global img_list
    global ink
    global image
    global index
    global operation
    global reloc_x
    global reloc_y
    global write
    global ink_enable
    global img_count
    img_list=[]
    vertices_list=[]
    
    file_name=store_path+'\img'+str(img_count)+'.jpg'
    img_count+=1
    
    cv2.imwrite(file_name,canvas)
    
    canvas[:,:]=(255,255,255)
    canvas[0:47,:]=toolbar
    
    write=-1
    ink,image,index,operation,reloc_x,reloc_y=-1,0,-1,-1,-1,-1
    ink_enable=-1

    
while(1):
    
    cv2.setMouseCallback('canvas',selection)
    
    if(image):
        cv2.imshow('gallery',gallery)
    
        cv2.setMouseCallback('gallery',page_selection)
        set_page()
        
    if(index!=-1):
        cv2.setMouseCallback('canvas',perform_operations)
    if(ink==1):
        cv2.setMouseCallback('canvas',ink_pen)
    
        
    if(new_canvas==1):
        save_canvas()
        new_canvas=-1
    cv2.imshow('canvas',canvas)
    if cv2.waitKey(1) & 0xFF==ord('w'):
        break
    
        
cv2.destroyAllWindows() 


# In[ ]:





# In[ ]:




