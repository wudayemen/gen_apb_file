#!/usr/bin/env python
# coding: utf-8

import xlrd
import re
import os
import sys
import math

# ==========================================================
#  func process excel                              start#{{{
# ==========================================================
def nullUp2Valid(p_sheet,p_row,p_col):#如果cell(row,col)为空，则用往上的格代替
    if(p_sheet.cell(p_row,p_col).ctype!=0):
        return p_sheet.cell(p_row,p_col).value
    else:
        return nullUp2Valid(p_sheet,p_row-1,p_col)

def getValueCol(p_sheet,p_value):#返回匹配值出现的第一个列数
    for row in range (p_sheet.nrows):
        for col in range (p_sheet.ncols):
            if(p_sheet.cell(row,col).value==p_value):
                return col
# ==========================================================
#  func process excel                                end#}}}
# ==========================================================

# ==========================================================
#  func process bit/bus/width                      start#{{{
# ==========================================================
def bit2width(var1):      #input '[8:7]' return 2;input without ':' return 1
    if(":" in var1):
        var1=var1.replace('[','')
        var1=var1.replace(']','')
        var1=var1.split(':')
        var1=int(var1[0])-int(var1[1])+1       
        return var1
    else:
        return 1

def width2bus(var1):     #input 2 return '[1:0]'; input 1 return ' '
    if(var1==1):
        return ''
    else:
        return '['+str(var1-1)+':0]'

def bus_width(var1):
    var1=bit2width(var1)
    var1=width2bus(var1)
    return var1
# ==========================================================
#  func process bit/bus/width                        end#}}}
# ==========================================================

#def wr_block
def wr_block(p_reg,p_fld,p_rst,p_bit):
    wr_str=[]
    wr_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wr_str.append("    if(!rst_n) begin\n")
    wr_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    wr_str.append("    end\n")
    wr_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    wr_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    wr_str.append("    end\n")
    wr_str.append("end\n")
    return wr_str

#def wrc_block
def wrc_block(p_reg,p_fld,p_rst,p_bit):
    wrc_str=[]
    wrc_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wrc_str.append("    if(!rst_n) begin\n")
    wrc_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    wrc_str.append("    end\n")
    wrc_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    wrc_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    wrc_str.append("    end\n")
    wrc_str.append("    else if(%s_wrc_clr) begin\n"%(p_fld.lower()))
    wrc_str.append("        %s <= %s_wrc_clr_val;\n"%(p_fld,p_fld))
    wrc_str.append("    end\n")
    wrc_str.append("end\n")
    return wrc_str

#def wrs_block
def wrs_block(p_reg,p_fld,p_rst,p_bit):
    wrs_str=[]
    wrs_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wrs_str.append("    if(!rst_n) begin\n")
    wrs_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    wrs_str.append("    end\n")
    wrs_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    wrs_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    wrs_str.append("    end\n")
    wrs_str.append("    else if(%s_wrs_set) begin\n"%(p_fld.lower()))
    wrs_str.append("        %s <= %s_wrs_set_val;\n"%(p_fld,p_fld))
    wrs_str.append("    end\n")
    wrs_str.append("end\n")
    return wrs_str
   
#def wo_block
def wo_block(p_reg,p_fld,p_rst,p_bit):
    wo_str=[]
    wo_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wo_str.append("    if(!rst_n) begin\n")
    wo_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    wo_str.append("    end\n")
    wo_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    wo_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    wo_str.append("    end\n")
    wo_str.append("end\n")
    return wo_str

#def w1_block
def w1_block(p_reg,p_fld,p_rst,p_bit):
    w1_str=[]
    w1_str.append("always@(posedge clk or negedge rst_n) begin\n")
    w1_str.append("    if(!rst_n) begin\n")
    w1_str.append("        %s_w1_done <= 1'b0;\n"%(p_fld))
    w1_str.append("    end\n")
    w1_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    w1_str.append("        %s_w1_done <= 1'b1;\n"%(p_fld))
    w1_str.append("    end\n")
    w1_str.append("end\n")
    w1_str.append("always@(posedge clk or negedge rst_n) begin\n")
    w1_str.append("    if(!rst_n) begin\n")
    w1_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    w1_str.append("    end\n")
    w1_str.append("    else if(%s_wr && (!%s_w1_done)) begin\n"%(p_reg.lower(),p_fld.lower()))
    w1_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    w1_str.append("    end\n")
    w1_str.append("end\n")
    return w1_str

#def wo1_block
def wo1_block(p_reg,p_fld,p_rst,p_bit):
    wo1_str=[]
    wo1_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wo1_str.append("    if(!rst_n) begin\n")
    wo1_str.append("        %s_wo1_done <= 1'b0;\n"%(p_fld))
    wo1_str.append("    end\n")
    wo1_str.append("    else if(%s_wr) begin\n"%(p_reg.lower()))
    wo1_str.append("        %s_wo1_done <= 1'b1;\n"%(p_fld))
    wo1_str.append("    end\n")
    wo1_str.append("end\n")
    wo1_str.append("always@(posedge clk or negedge rst_n) begin\n")
    wo1_str.append("    if(!rst_n) begin\n")
    wo1_str.append("        %s <= %s'%s;\n"%(p_fld,bit2width(p_bit),p_rst))
    wo1_str.append("    end\n")
    wo1_str.append("    else if(%s_wr && (!%s_wo1_done)) begin\n"%(p_reg.lower(),p_fld.lower()))
    wo1_str.append("        %s <= pwdata%s;\n"%(p_fld,p_bit))
    wo1_str.append("    end\n")
    wo1_str.append("end\n")
    return wo1_str

##################
def rd_block(p_reg,p_address):
    rd_str=[]
    p_address = p_address.replace('0x','8\'h').replace('0X','8\'h')
    rd_str.append("%8s%s : prdata = %-10s;\n"%('',p_address,p_reg.upper()))
    return rd_str


# ==========================================================
#  int_logic                                       start#{{{
# ==========================================================
def int_logic(p_sheet):
    int_str = []
    fld_col = getValueCol(p_sheet,'FieldName')
    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        if(fld_name.endswith('_int')):
                int_str.append(" | (%s & %s_en)"%(fld_name,fld_name))
    return int_str
# ==========================================================
#  int_logic                                         end#}}}
# ==========================================================

# ==========================================================
#  gen_reg_hdl                                     start#{{{
# ==========================================================
def gen_reg_hdl(p_sheet,ModuleName):
    base_col = getValueCol(p_sheet,'BaseAddress')
    base_value = p_sheet.cell(1,base_col).value.replace('0x','32\'h').replace('0X','32\'h')

    width_col = getValueCol(p_sheet,'Width')
    width_value = int(p_sheet.cell(1,width_col).value)
    data_bus_width = width2bus(width_value)
    
    
    reg_col = getValueCol(p_sheet,'RegName')
    fld_col = getValueCol(p_sheet,'FieldName')
    rst_col = getValueCol(p_sheet,'ResetValue')
    bit_col = getValueCol(p_sheet,'Bits')
    access_col  = getValueCol(p_sheet,'Access')
    adr_col  = getValueCol(p_sheet,'OffsetAddress')

    fo=open("%s_apb_cfg.v"%(ModuleName),"w")
    fo.write("module %s_apb_cfg ("%(ModuleName))
    fo.write("\n"+16*" "+" clk")
    fo.write("\n"+16*" "+",rst_n")
    fo.write("\n"+16*" "+",pwrite")
    fo.write("\n"+16*" "+",psel")
    fo.write("\n"+16*" "+",penable")
    fo.write("\n"+16*" "+",paddr")
    fo.write("\n"+16*" "+",pwdata")
    fo.write("\n"+16*" "+",prdata")
    #insert other port
    as_is_list = ['RW','WRC','WRS','WO','W1','WO1']
    
    w1c_list =['W1C','W1CRS']
    w0c_list =['W0C','W0CRS']
    w1s_list =['W1S','W1SRC']
    w0s_list =['W0S','W0SRC']
    w1t_list =['W1T']
    w0t_list =['W0T']

    wc_list = ['WC','WCRS','WOC']
    ws_list = ['WS','WSRC','WOS']
    rc_list = ['RC','WRC','WSRC','W1SRC','W0SRC']
    rs_list = ['RS','WRS','WCRS','W1CRS','W0CRS']

    
    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() != 'reserved'):
            if(fld_type in as_is_list):
                fo.write("\n"+16*" "+","+fld_name)
            else:
                fo.write("\n"+16*" "+","+fld_name)

            if(fld_type in w1c_list):
                fo.write("\n"+16*" "+",%s_%s_clr"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_clr_val"%(fld_name,fld_type.lower()))
            if(fld_type in w0c_list):
                fo.write("\n"+16*" "+",%s_%s_clr"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_clr_val"%(fld_name,fld_type.lower()))
            if(fld_type in w1s_list):
                fo.write("\n"+16*" "+",%s_%s_set"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_set_val"%(fld_name,fld_type.lower()))
            if(fld_type in w0s_list):
                fo.write("\n"+16*" "+",%s_%s_set"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_set_val"%(fld_name,fld_type.lower()))
            if(fld_type in w1t_list):
                fo.write("\n"+16*" "+",%s_%s_tog"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_tog_val"%(fld_name,fld_type.lower()))
            if(fld_type in w0t_list):
                fo.write("\n"+16*" "+",%s_%s_tog"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_tog_val"%(fld_name,fld_type.lower()))


            if(fld_type in wc_list):
                fo.write("\n"+16*" "+",%s_%s_clr"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_clr_val"%(fld_name,fld_type.lower()))
            if(fld_type in rc_list and fld_type != 'WRC'):
                fo.write("\n"+16*" "+",%s_%s_clr"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_clr_val"%(fld_name,fld_type.lower()))
            if(fld_type in ws_list):
                fo.write("\n"+16*" "+",%s_%s_set"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_set_val"%(fld_name,fld_type.lower()))
            if(fld_type in rs_list and fld_type != 'WRS'):
                fo.write("\n"+16*" "+",%s_%s_set"%(fld_name,fld_type.lower()))
                fo.write("\n"+16*" "+",%s_%s_set_val"%(fld_name,fld_type.lower()))
    fo.write("\n"+16*" "+");")
    fo.write("\n")

    
    #signal direction declare
    fo.write("input           clk;\n")
    fo.write("input           rst_n;\n")
    fo.write("input           pwrite;\n")
    fo.write("input           psel;\n")    
    fo.write("input           penable;\n")    
    fo.write("input  [31:0]   paddr;\n")
    fo.write("input  %-9s%s;\n"%(data_bus_width,'pwdata'))
    fo.write("output %-9s%s;\n"%(data_bus_width,'prdata'))
    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() != 'reserved'):
            if(fld_type in as_is_list):
                fo.write("output %-9s%s;\n"%(bus_width(bit),fld_name))
            else:
                fo.write("input  %-9s%s;\n"%(bus_width(bit),fld_name))
            
            if(fld_type in w1c_list):
                fo.write("output %-9s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0c_list):
                fo.write("output %-9s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w1s_list):
                fo.write("output %-9s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0s_list):
                fo.write("output %-9s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w1t_list):
                fo.write("output %-9s%s_%s_tog;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_tog_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0t_list):
                fo.write("output %-9s%s_%s_tog;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_tog_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            
            if(fld_type in wc_list):
                fo.write("output %-9s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in rc_list and fld_type != 'WRC'):
                fo.write("output %-9s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in ws_list):
                fo.write("output %-9s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in rs_list and fld_type != 'WRS'):
                fo.write("output %-9s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("output %-9s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))

     ####################################20200713                       
     #signal type declare
    fo.write("wire            clk;\n")
    fo.write("wire            rst_n;\n")
    fo.write("wire            pwrite;\n")
    fo.write("wire            psel;\n")    
    fo.write("wire            penable;\n")    
    fo.write("wire [31:0]     paddr;\n")    
    fo.write("wire %-11s%s;\n"%(data_bus_width,'pwdata'))
    fo.write("reg  %-11s%s;\n"%(data_bus_width,'prdata'))
    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() != 'reserved'):
            if(fld_type in as_is_list):
                fo.write("reg  %-11s%s;\n"%(bus_width(bit),fld_name))
            else:
                fo.write("wire %-11s%s;\n"%(bus_width(bit),fld_name))

            if(fld_type in w1c_list):
                fo.write("wire %-11s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0c_list):
                fo.write("wire %-11s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w1s_list):
                fo.write("wire %-11s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0s_list):
                fo.write("wire %-11s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w1t_list):
                fo.write("wire %-11s%s_%s_tog;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_tog_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in w0t_list):
                fo.write("wire %-11s%s_%s_tog;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_tog_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            
            if(fld_type in wc_list):
                fo.write("wire %-11s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in rc_list):
                fo.write("wire %-11s%s_%s_clr;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_clr_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in ws_list):
                fo.write("wire %-11s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
            if(fld_type in rs_list):
                fo.write("wire %-11s%s_%s_set;\n"%('',fld_name,fld_type.lower()))
                fo.write("wire %-11s%s_%s_set_val;\n"%(bus_width(bit),fld_name,fld_type.lower()))
    

    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_type == 'W1'):
            fo.write("reg  %-11s%s_w1_done;\n"%('',fld_name))
        if(fld_type == 'WO1'):
            fo.write("reg  %-11s%s_wo1_done;\n"%('',fld_name))



    #reg_declared
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("wire %-11s%s;\n"%(data_bus_width,reg_name.upper()))
    #reg_wr=paddr&wr
    #reg_rd=paddr&rd
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("wire %-11s%s_wr;\n"%('',reg_name.lower()))
            fo.write("wire %-11s%s_rd;\n"%('',reg_name.lower()))

    #insert apb-->reg_wr,reg_rd.
    fo.write("wire %-11sreg_wr;\n"%(''))
    fo.write("wire %-11sreg_rd;\n"%(''))
    fo.write("assign reg_wr = psel & pwrite & penable;\n")
    fo.write("assign reg_rd = psel & (~pwrite) & (~penable);\n")
    
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        address = nullUp2Valid(p_sheet,row,adr_col).replace('0x','8\'h').replace('0X','8\'h')
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("assign %s_wr = (paddr == %s) & reg_wr;\n"%(reg_name.lower(),base_value+' + '+address))
            fo.write("assign %s_rd = (paddr == %s) & reg_rd;\n"%(reg_name.lower(),base_value+' + '+address))
  
     #################################################20200707 sheetchange

    #assign REG[1]=fld
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        rst_value = p_sheet.cell(row,rst_col).value
        rst_value = re.search('[bodh][a-f0-9]+$',rst_value).group()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() == 'reserved' or fld_type == 'WO' or fld_type == 'WOC' or fld_type == 'WOS' or fld_type == 'WO1'):
            fo.write("assign %s%s = %s\'%s;\n"%(reg_name.upper(),bit,bit2width(bit),rst_value))
        else:
            fo.write("assign %s%s = %s;\n"%(reg_name.upper(),bit,fld_name))
    #main logic for w1c
    for row in range (p_sheet.nrows)[1:]:
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        if(fld_name.lower() != 'reserved'):
            if(fld_type in w1c_list):
                fo.write("assign %s_%s_clr = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_clr_val%s =%s%s &(~pwdata%s);\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            if(fld_type in w0c_list):
                fo.write("assign %s_%s_clr = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_clr_val%s =%s%s & pwdata%s;\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            if(fld_type in w1s_list):
                fo.write("assign %s_%s_set = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_set_val%s =%s%s | pwdata%s;\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            if(fld_type in w0s_list):
                fo.write("assign %s_%s_set = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_set_val%s =%s%s |(~pwdata%s);\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            if(fld_type in w1t_list):
                fo.write("assign %s_%s_tog = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_tog_val%s =%s%s ^ pwdata%s;\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            if(fld_type in w0t_list):
                fo.write("assign %s_%s_tog = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_tog_val%s =%s%s ^(~pwdata%s);\n"%(fld_name,fld_type.lower(),bus_width(bit),fld_name,bus_width(bit),bit))
            
            if(fld_type in wc_list):
                fo.write("assign %s_%s_clr = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_clr_val%s =%s'b0;\n"%(fld_name,fld_type.lower(),bus_width(bit),bit2width(bit)))
            if(fld_type in rc_list):
                fo.write("assign %s_%s_clr = %s_rd;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_clr_val%s =%s'b0;\n"%(fld_name,fld_type.lower(),bus_width(bit),bit2width(bit)))
            if(fld_type in ws_list):
                fo.write("assign %s_%s_set = %s_wr;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_set_val%s =%s'b%s;\n"%(fld_name,fld_type.lower(),bus_width(bit),bit2width(bit),pow(2,bit2width(bit))-1))
            if(fld_type in rs_list):
                fo.write("assign %s_%s_set = %s_rd;\n"%(fld_name,fld_type.lower(),reg_name.lower()))
                fo.write("assign %s_%s_set_val%s =%s'b%s;\n"%(fld_name,fld_type.lower(),bus_width(bit),bit2width(bit),pow(2,bit2width(bit))-1))


#######################20200722##########################
    #main logic reg_int
    #fo.write("assign reg_int = 1'b0%s;\n"%("".join(int_logic(p_sheet))))
    #main logic Wr
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        rst_value = p_sheet.cell(row,rst_col).value
        rst_value = re.search('[bodh][a-f0-9]+$',rst_value).group()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() != 'reserved'):
            if(fld_type == 'RW'): 
                fo.write("".join(wr_block(reg_name,fld_name,rst_value,bit)))
            if(fld_type == 'WRC'): 
                fo.write("".join(wrc_block(reg_name,fld_name,rst_value,bit)))
            if(fld_type == 'WRS'): 
                fo.write("".join(wrs_block(reg_name,fld_name,rst_value,bit)))
            if(fld_type == 'WO'): 
                fo.write("".join(wo_block(reg_name,fld_name,rst_value,bit)))
            if(fld_type == 'W1'): 
                fo.write("".join(w1_block(reg_name,fld_name,rst_value,bit)))
            if(fld_type == 'WO1'): 
                fo.write("".join(wo1_block(reg_name,fld_name,rst_value,bit)))

    #main logic Rd
    fo.write("always@(*) begin\n")
    fo.write("    case(paddr)\n")
    #fo.write("".join(rd_logic(p_sheet)))
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        address = nullUp2Valid(p_sheet,row,adr_col).replace('0x','8\'h').replace('0X','8\'h')
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("".join(rd_block(reg_name,base_value+' + '+address)))
    fo.write("        default:prdata = %s'b0;\n"%(width_value))
    fo.write("    endcase\n")
    fo.write("end\n")
    fo.write("endmodule")
    fo.close()
    print("Successfully generated %s_apb_cfg.v"%(ModuleName))
# ==========================================================
#  gen_reg_hdl                                       end#}}}
# ==========================================================
# ==========================================================
#  gen_reg_cheader                                 start#{{{
# ==========================================================

def gen_reg_cheader(p_sheet,ModuleName):
    base_col = getValueCol(p_sheet,'BaseAddress')
    base_value = p_sheet.cell(1,base_col).value

    reg_col = getValueCol(p_sheet,'RegName')
    fld_col = getValueCol(p_sheet,'FieldName')
    rst_col = getValueCol(p_sheet,'ResetValue')
    bit_col = getValueCol(p_sheet,'Bits')
    access_col  = getValueCol(p_sheet,'Access')
    adr_col  = getValueCol(p_sheet,'OffsetAddress')

    fo=open("%s.h"%(ModuleName),"w")
    fo.write("#ifndef __TYPE_H__\n")
    fo.write("#define __TYPE_H__\n")
    fo.write("\n")
    fo.write("#define REG32(_register_) (*(volatile unsigned int *)(_register_))\n")
    fo.write("#define REG8(_register_)  (*(volatile unsigned char *)(_register_))\n") 
    fo.write("\n") 
    fo.write("#endif\n") 
    fo.write("\n")
    
    fo.write("/************************** Constant Definitions *****************************/\n")
    fo.write("#ifndef __%s_H__\n"%(ModuleName.upper()))
    fo.write("#define __%s_H__\n"%(ModuleName.upper()))
    fo.write("\n")
    fo.write("#define %-19s %s\n"%(ModuleName.upper()+'_BASEADDR',base_value))
    for row in range (p_sheet.nrows)[1:]:
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        address = nullUp2Valid(p_sheet,row,adr_col)#.replace('0x','8\'h').replace('0X','8\'h')
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("#define %-19s (%s_BASEADDR + %s)\n"%(reg_name.upper()+'_ADDR',ModuleName.upper(),address))
 
    fo.write("\n")
    fo.write("#endif\n")
    fo.close()
    print("Successfully generated %s.h"%(ModuleName))

# ==========================================================
#  gen_reg_cheader                                   end#}}}
# ==========================================================

def gen_reg_ralf(p_sheet,ModuleName):
    base_col = getValueCol(p_sheet,'BaseAddress')
    base_value = p_sheet.cell(1,base_col).value

    width_col = getValueCol(p_sheet,'Width')
    width_value = int(p_sheet.cell(1,width_col).value)

    reg_col = getValueCol(p_sheet,'RegName')
    fld_col = getValueCol(p_sheet,'FieldName')
    rst_col = getValueCol(p_sheet,'ResetValue')
    bit_col = getValueCol(p_sheet,'Bits')
    access_col  = getValueCol(p_sheet,'Access')
    adr_col  = getValueCol(p_sheet,'OffsetAddress')

    fo=open("%s.ralf"%(ModuleName),"w")
    fo.write("#write below command in Makefile\n")
    fo.write("#ralgen:\n")
    fo.write("#    ralgen -l sv  -uvm  -t  %s_regmodel  %s.ralf\n"%(ModuleName,ModuleName))
    fo.write("#use 'source %s.ralf' in top.ralf\n"%(ModuleName))
    last_reg_name = ''
    i = 0
    fo.write("#")
    for row in reversed(range (p_sheet.nrows)[1:]):
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        rst_value = p_sheet.cell(row,rst_col).value
        rst_value = re.search('[bodh][a-f0-9]+$',rst_value).group()
        bit       = p_sheet.cell(row,bit_col).value
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(fld_name.lower() != 'reserved'):
            if(reg_name != last_reg_name):
                fo.write("}\n")
                fo.write("\n")
                fo.write("register %s {\n"%(reg_name.upper()))
                fo.write("#  ToDo\n")
            last_reg_name = reg_name;
            fo.write("  field %s {\n"%(fld_name))
            fo.write("    bits %s;\n"%(bit2width(bit)))
            fo.write("    access %s;\n"%(fld_type.lower()))
            fo.write("    reset '%s;\n"%(rst_value))
            fo.write("  }\n")

        elif(fld_name.lower() == 'reserved'):
            if(reg_name != last_reg_name):
                fo.write("}\n")
                fo.write("\n")
                fo.write("register %s {\n"%(reg_name.upper()))
                fo.write("#  ToDo\n")
            last_reg_name = reg_name;
            i=i+1;
            fo.write("  field reserved%s {\n"%(i))
            fo.write("    bits %s;\n"%(bit2width(bit)))#different here
            fo.write("    access %s;\n"%(fld_type.lower()))
            fo.write("    reset '%s;\n"%(rst_value))
            fo.write("  }\n") 
    fo.write("}\n")
    
    fo.write("\n")
    fo.write("block %s_regmodel {\n"%(ModuleName))
    fo.write("  bytes %s;\n"%(width_value/8))
    for row in reversed(range (p_sheet.nrows)[1:]):
        reg_name  = nullUp2Valid(p_sheet,row,reg_col)
        fld_name  = p_sheet.cell(row,fld_col).value.lower()
        rst_value = p_sheet.cell(row,rst_col).value
        rst_value = re.search('[bodh][a-f0-9]+$',rst_value).group()
        bit       = p_sheet.cell(row,bit_col).value
        address   = p_sheet.cell(row,adr_col).value.replace('0x','h').replace('0X','h')
        fld_type  = nullUp2Valid(p_sheet,row,access_col)
        if(p_sheet.cell(row,adr_col).value!=''):
            fo.write("  register %-13s %-15s @'%s;\n"%(reg_name.upper(),"("+reg_name.lower()+")",address))

    fo.write("}\n")
    fo.write("\n")
    fo.close()
    print("Successfully generated %s.ralf"%(ModuleName))
 
#max_rows=sheet0.nrows#行数
#max_cols=sheet0.ncols#列数
if(len(sys.argv) < 2):
    print("[Error]:Not have input file")
    print("Usage : %s <filename>.xlsx"%(sys.argv[0]))
    sys.exit(1)

if(sys.argv[1]=='-help'):
    print("Usage : %s <filename>.xlsx"%(sys.argv[0]))
    sys.exit(0)

if(os.path.exists(sys.argv[1])==False):
    print("[Error]:Not such file")
    sys.exit(1)


book = xlrd.open_workbook(sys.argv[1])
sheets_num = len(book.sheet_names())
for index in range (sheets_num):
    sheet0 = book.sheet_by_index(index)
    ModuleName = sheet0.name
    #ModuleName  = re.search('^[a-z]+',sys.argv[1]).group()#从开头位置开始匹配返回第一个，而findall返回一个list
    gen_reg_hdl(sheet0,ModuleName)
    gen_reg_cheader(sheet0,ModuleName)
    gen_reg_ralf(sheet0,ModuleName)
sys.exit(0)

