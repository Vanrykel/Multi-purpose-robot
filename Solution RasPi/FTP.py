
# coding: utf-8

# In[1]:


from ftplib import FTP
import os


# In[2]:


session = FTP('username','password')
file = open('jason.txt','rb')                  # file to send
session.storbinary('STOR jason.txt', file)     # send the file
file.close()                                    # close file and FTP
session.quit()

