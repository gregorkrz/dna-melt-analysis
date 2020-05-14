import random
import string
import time
import xlsxwriter
from globals import *

class ExcelWriter:
  def __init__(self, save=True):
    self.filename = randomFileName('out/', 'xlsx')
    self.workbook = xlsxwriter.Workbook(self.filename)
    self.column = 0
    self.save=save
  def addWorksheet(self, ws):
      self.worksheet = self.workbook.add_worksheet(ws)
  def writeCol(self, col):
      for c in range(len(col)):
        self.worksheet.write(c, self.column, col[c])
      self.column += 1
  def writeTable(self, table, titles):
      for i in range(len(titles)):
          self.writeCol([titles[i]]+table[i])


  def close(self):
      if self.save:
        self.workbook.close()
        print("Plot saved to file", self.filename)


def randomFileName(start="", ending="txt"):
    return start+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))+"."+ending


def all_same(items):
    return all(x == items[0] for x in items)
