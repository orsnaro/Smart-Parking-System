import tkinter as tk
import ocr_cv
import random
import communicatoin as arduino
import Garage_DB as db


def park_wait_page():

    global l_8
    global done_b

    # define page
    global p_page_2
    p_page_2 = tk.Tk()
    p_page_2.configure(bg='#000F35')
    p_page_2.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_2.title("parking Page.2")
    #################################


    # wait word
    l_3 = tk.Label(p_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
    l_3.place(x=(screen_w / 2)-240, y=(screen_h / 2)-150)


    def done():
        l_8.destroy()
        done_b.destroy()

        l_9 = tk.Label(p_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
        l_9.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

        def park():
            '''arduino code'''
            try:
                arduino.park(user_info['park_cell'])
            except:
                print('error in arduino')
            #########################
            l_9.destroy()
            l_4 = tk.Label(p_page_2, text='DONE', font=('Arial', 150, 'bold'), bg='#000F35', fg='#04B400', borderwidth=0)
            l_4.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

            def destroy_l():
                p_page_2.destroy();root_page()

            p_page_2.after(5000, destroy_l)

        p_page_2.after(100, park)

    def park_now():
        '''arduino code'''
        try :
            arduino.prepare_for_parknig(user_info['park_cell'])
        except:
            print('error in arduino prepare')
        #########################
        l_3.destroy()

        global l_8
        global done_b

        l_8 = tk.Label(p_page_2, text='Park car now', font=('Arial', 50, 'bold'), bg='#000F35', fg='#FAFF00',borderwidth=0)
        l_8.place(x=(screen_w / 2) - 100, y=(screen_h / 4))

        done_b = tk.Button(p_page_2, text='Done', font=('Arial', 14, 'bold'), bg='#04B400', fg='white',borderwidth=0)
        done_b.configure(command=done)
        done_b.place(x=(screen_w / 2) - 70, y=(screen_h / 2) + 50, width=140, height=40)

    # will change to 10 after add arduino
    p_page_2.after(1000,park_now)

    p_page_2.mainloop()
def park_page_1():
    #define page
    global p_page_1
    p_page_1 = tk.Tk()
    p_page_1.configure(bg='#000F35')
    p_page_1.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_1.title("parking Page.1")
    #################################

    # show password
    l_1 = tk.Label(p_page_1,text='Please save this password',font=('Arial',12),bg='#000F35',fg='#FF4141', borderwidth=0)
    l_1.place(x=(screen_w/2)-90,y=(screen_h/4)-100)


    password = str(random.randint(1000,9999))

    user_info['password']= password
    l_2 = tk.Label(p_page_1,text=f'{password}',font=('Arial',90,'bold'),bg='#000F35',fg='#FAFF00', borderwidth=0)
    l_2.place(x=(screen_w / 2)-125, y=(screen_h / 4))
    #####################

    def b_park_2():
        p_page_1.destroy()
        '''add user_info to DB'''

        user_info['park_cell']=db.db_cmd(0,user_info['id'],password)

        #########################
        park_wait_page()


    # define continue parking button
    park_2 = tk.Button(p_page_1, text='Park Now',font=('Arial',14,'bold'),bg='#04B400',fg='white', borderwidth=0)
    park_2.configure(command=b_park_2)
    park_2.place(x=(screen_w/2)-70,y=(screen_h/2)+50,width=140,height=40)
    ###################################

    def b_cancel(): p_page_1.destroy();root_page()

    # define cancel button
    cancel = tk.Button(p_page_1, text='Cancel',font=('Arial',14,'bold'),bg='#D40101',fg='white', borderwidth=0)
    cancel.configure(command=b_cancel)
    cancel.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=140,height=40)
    ###################################

    p_page_1.mainloop()

def park_button():
    if(db.db_cmd(2)) :
        return 0

    root.destroy()
    ocr_cv.testing_mode = False
    #id = ocr_cv.ocr_main()
    id=('11111111111111',True)
    user_info['id']=id[0]

    if(id[1]):
        park_page_1()
    else:
        root_page()



def pay_page():
    print(ocr_info[0])
    get_info = db.db_cmd(1,ocr_info[0])

    if(not get_info[1]):
        get_car_page()
        return 0

    global pay_p
    pay_p = tk.Tk()
    pay_p.title("Hello car")
    pay_p.configure(bg='#000F35')
    pay_p.geometry(f"{screen_w}x{screen_h}")


    tk.Label(pay_p,text=f"Time: {get_info[3]}  hours ",font=('Arial',15,'bold'),bg='black',fg='purple').place(x=(screen_w / 2) - 70, y=(screen_h / 4))
    tk.Label(pay_p,text=f"cost:  {get_info[2]}  $",font=('Arial',15,'bold'),bg='black',fg='purple').place(x=(screen_w / 2) - 70, y=(screen_h / 4) )
    pay_b=tk.Button(pay_p,
               text="pay",
                font=('Arial', 14, 'bold'),
                bg='#04B400',
                fg='white',
                borderwidth=0,
                )
    pay_b.place(x=(screen_w / 2) - 70, y=(screen_h / 4) * 3 - 50, width=140, height=40)

    pay_p.mainloop()

def get_car_page():
  global get_car

  get_car=tk.Tk()
  get_car.title("get car")
  get_car.configure(bg='#000F35')
  get_car.geometry(f"{screen_w}x{screen_h}")

  def face():
      get_car.destroy()

      '''OCR'''
      ocr_cv.testing_mode = False

      global ocr_info
      #ocr_info = ocr_cv.ocr_main()
      ocr_info=('11111111111111',True)

      if (ocr_info[1]):
         pay_page()
      else:
          get_car_page()
      ##############



  tk.Label(get_car,
       text="Get it by",font=('Arial',30,'bold'),bg='#000F35',fg='#FF0000').place(x=(screen_w/8),y=(screen_h/2)-100)

  btn1=tk.Button(get_car,
                text="ID Card",
                font=('Arial', 14, 'bold'),
                bg='#04B400',
                fg='white', borderwidth=0,
                command=face)
  btn1.place(x=(screen_w/3),y=(screen_h/2)-90,width=140,height=40)


  btn2=tk.Button(get_car,
                text="password",
                font=('Arial', 14, 'bold'),
                bg='#04B400',
                fg='white', borderwidth=0)
  btn2.place(x=(screen_w/3)*2-20,y=(screen_h/2)-90,width=140,height=40)


  def cancel():
        get_car.destroy()
        root_page()

  btn3=tk.Button(get_car,
                text="Cancel",
                font = ('Arial', 14, 'bold'),
                bg = '#D40101',
                fg = 'white',
                borderwidth = 0,
                command=cancel)
  btn3.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=140,height=40)

  get_car.mainloop()

def root_page():
    global root
    root = tk.Tk()

    # Get the screen geometry
    global screen_w
    global screen_h
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Set the dimensions of the root
    root.configure(bg='#000F35')
    root.geometry(f"{screen_w}x{screen_h}+0+0")

    root.title("Home Page")

    # check parking isfull
    if (db.db_cmd(2)):
        l_6 = tk.Label(root, text='parking is full', font=('Arial', 5, 'bold'), bg='#000F35', fg='red', borderwidth=0)

        l_6.place(x=100, y=100)


    #define parking button
    b_park = tk.Button(root, text='Park',font=('Arial',14,'bold'),bg='#04B400',fg='white', borderwidth=0)
    b_park.configure(command=park_button)
    b_park.place(x=(screen_w/2)-70,y=(screen_h/2)-50,width=140,height=40)
    ###################################

    def get_car_button(): root.destroy();get_car_page()
    #define getcar button
    b_get = tk.Button(root, text='GetCar',font=('Arial',14,'bold'),bg='#D40101',fg='white', borderwidth=0)
    b_get.configure(command=get_car_button)
    b_get.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=140,height=40)
    ###################################


    root.mainloop()



if __name__ == "__main__":

    user_info ={'id':None,'password':None,'park_cell':None}
    root_page()
