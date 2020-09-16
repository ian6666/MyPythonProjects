import os
from fpdf import FPDF

def check_ans(key,score,line):
    temp = []
    num_correct = 0
    ind = 0
    wrongs = []
    for a in range(len(key)):
        if(key[a].lower()==line[a].lower()):
            num_correct += 1
        else:
            wrongs.append(str(ind+1))
        ind+=1
    temp.append(wrongs)
    temp.append(int(num_correct/len(key)*100))
    temp.append(num_correct)
    temp.append(int(score[num_correct]))
    
    return temp

##----------------------------------------------------------------------------
def student_report(Class):
        
    for ID in Class:

        if ID=="TestName":
            continue
        
        pdf = FPDF('P','mm','Letter')
        pdf.add_page()
        
        pdf.set_font('Times', 'B', 18)
        pdf.set_y(20)
        pdf.cell(190, 10, Class["TestName"],1,1,'C')
        
        pdf.set_font('Times', 'B', 14)
        pdf.set_xy(20,40)
        pdf.cell(60, 10, 'ID: ' + ID, 0, 0, 'L')
        pdf.cell(60, 10, 'Name: '+Class[ID]['Name'], 0, 0, 'L')
        pdf.cell(60, 10, 'Total: ' + str(Class[ID]["Grade"]), 0, 1, 'L')
        
        i = 1
        for k in Class[ID]:
            if k in ["Math","CR","WR"]:
                pdf.set_font('Times', 'B', 14)
                pdf.set_xy(20,60*i)
                pdf.cell(60, 10, 'Section: ' + k, 0, 0, 'L')
                pdf.cell(60, 10, 'Score: ' + str(Class[ID][k][3]), 0, 1, 'L')
                
                pdf.set_font('Times', 'B', 12)
                pdf.cell(20)
                correct = str(Class[ID][k][2])
                pdf.cell(60, 10, 'Correct #: ' + correct, 0, 1, 'L')
                pdf.cell(20)
                w = ", ".join(Class[ID][k][0])
                pdf.cell(20, 10, 'Wrongs: ', 0, 0, 'L')
                pdf.multi_cell(150, 10, w, 0, 1, 'L')
                i+=1
                
        pdf.output(Class[ID]['Name'] +'.pdf', 'F')


##----------------------------------------------------------------------------
def student_subject(Class,subject):
    
    pdf = FPDF('P','mm','Letter')
    pdf.add_page()
    
    pdf.set_font('Times', 'B', 18)
    pdf.set_y(20)
    pdf.cell(190, 10, Class["TestName"]+' '+subject+' By Student Summary',1,1,'C')
    
    limit = 7
    count = 0
    for ID in Class:
        if ID=="TestName":
            continue
        
        if count==limit:
            pdf.add_page()
            count=0
        pdf.set_font('Times', 'B', 14)
        j=count%7
        y = 40 + (j*30)
        pdf.set_xy(20,y)
        pdf.cell(60, 10, 'Name: '+Class[ID]['Name'],0, 0, 'L')
        pdf.cell(60, 10, 'Score: '+str(Class[ID]['Grade']), 0, 1, 'L')
        
        pdf.set_font('Times', 'B', 12)
        pdf.cell(20)
        pdf.cell(20, 10, 'Wrongs:', 0, 0, 'L')
        wrongs = ", ".join(Class[ID][subject][0])
        pdf.multi_cell(150, 10, wrongs, 0, 1, 'L')
        count+=1

    pdf.output(subject+'_by_student.pdf', 'F')


##----------------------------------------------------------------------------
def teacher_report(Class,subject,key):
    
    w_stat = {str(i):0 for i in range(1,len(key)+1)}
        
    for ID in Class:
        if ID=="TestName":
            continue
        for w in Class[ID][subject][0]:
            w_stat[w]+=1
    
    pdf = FPDF('P','mm','Letter')
    pdf.add_page()
    
    pdf.set_font('Times', 'B', 18)
    pdf.set_y(20)
    pdf.cell(190, 10, Class["TestName"]+' '+subject+' Summary',1,1,'C')
    
    totalQ = len(key)
    limit = 15
    rows = (totalQ//limit)+1
    pdf.set_xy(35,50)
    count1 = 1
    count2 = 1
    count3 = 1
    
    for j in range(rows*3):
    
        if j%3==0:
            for i in range(limit):
                if count1>totalQ:
                    break
                else:
                    pdf.set_font('Times', 'B', 12)
                    pdf.cell(10, 10, str(count1), 1, 0, 'C')
                    count1+=1
        elif j%3 == 1:
            for i in range(limit):
                if count2>totalQ:
                    break
                else:
                    pdf.set_font('Times', '', 12)
                    pdf.cell(10, 10, key[count2-1], 1, 0, 'C')
                    count2+=1
        else:
            for i in range(limit):
                if count3>totalQ:
                    break
                else:
                    pdf.set_font('Times', '', 12)
                    pdf.cell(10, 10, str(w_stat[str(count3)]), 1, 0, 'C')
                    count3+=1
                
        pdf.ln()
        pdf.cell(25)
    
    pdf.output(subject+'_summary.pdf', 'F')
    

##----------------------------------------------------------------------------
##  Get student database
stdb_file = open('Student Database.csv','r')

students = {}
for line in stdb_file:
    line = line.strip().split(",")
    students[line[0]] = line[1] + " " +line[2]

stdb_file.close()
    
##  Get SAT Test Keys
key_file = open('key.csv','r')

key_table = []
testName = key_file.readline().strip()
math_key = key_file.readline().strip().split(",")#Math Key
math_key.pop(0)
math_key.pop(0)
cr_key = key_file.readline().strip().split(",")#Reading key
cr_key.pop(0)
cr_key.pop(0)
wr_key = key_file.readline().strip().split(",")#Writing key
wr_key.pop(0)
wr_key.pop(0)  

key_file.close()  
    
##  Get SAT Test Conversion Scores    
sc_file = open('scores.csv','r')

math_sc = sc_file.readline().strip().split(",")
math_sc.pop(0)
cr_sc = sc_file.readline().strip().split(",")
cr_sc.pop(0)
wr_sc = sc_file.readline().strip().split(",")
wr_sc.pop(0)      
    
sc_file.close()  

##  Get Students answers and check the result
entries = os.listdir('Student_tests/')
SAT_class = {}

for entry in entries:
    ans_file = open("Student_tests/"+entry,'r')
    ans_file.readline() #first line no useful info
    
    SAT_score = 0
    st = {}
    for line in ans_file:
        line = line.strip().split(",")    
        ID = line.pop(0)
        section = line.pop(0)
        
        if section == "Math":
            key = math_key
            score = math_sc
        if section == "CR":
            key = cr_key
            score = cr_sc
        if section == "WR":
            key = wr_key
            score = wr_sc
            
        checked = check_ans(key,score,line)
        st[section] = checked
        SAT_score += checked[-1]
        
    st["Name"] = students[ID]
    st["Grade"] = SAT_score
    SAT_class[ID] = st
    SAT_class["TestName"] = testName

##  Generate Reports for Students and Teacher        
student_report(SAT_class)
student_subject(SAT_class,'Math')
student_subject(SAT_class,'CR')
student_subject(SAT_class,'WR')
teacher_report(SAT_class,'Math',math_key)
teacher_report(SAT_class,'CR',cr_key)
teacher_report(SAT_class,'WR',wr_key)