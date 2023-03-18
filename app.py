from flask import Flask,render_template,request
import requests
import time
from random import randint
import json
import pathlib
from os.path import isfile, join
from os import listdir
import random
import pickle

# with open("./cybertotal_name_desc.txt","r",encoding="UTF-8") as f:
#     cybertotal_list = f.readlines()
# with open("./cybertotal_name_desc_out.txt","r",encoding="UTF-8") as f:
#     todo_list = f.readlines()

# cybertotal_list = list(filter(lambda item: item != "\n" , cybertotal_list))
# todo_list = list(filter(lambda item: item != "\n" , todo_list))
# uid_list = []
# str_list = []
# bio_list = []
# for i in range(0,len(todo_list)):
#     if i % 3 == 0:
#         uid_list.append(todo_list[i])
#     elif i % 3 == 1:
#         str_list.append(todo_list[i])
#     else:
#         bio_list.append(todo_list[i])
# valid_sample_count = 0
# ner_token = {"HackOrg":0,"OffAct":0,"SamFile":0,"SecTeam":0,"Tool":0,"Time":0,"Purp":0,"Area":0,"Idus":0,"Org":0,"Way":0,"Exp":0,"Features":0,"O":0,"X":0}
# for i in range(len(bio_list)):
#     tokens = bio_list[i].split()
#     for token in tokens:
#         if token != "O" and token != "X" and token !="":
#             ner_token[token.split("-")[1]] += 1
#         elif token == "O":
#             ner_token["O"] += 1
#         elif token == "X":
#             ner_token["X"] += 1
# new_dic = {}
# for i in range(0,len(uid_list)):
#     file_path = "../cybertotal/detail/"+ uid_list[i].replace("\n", "").replace("   ", "  ").replace("  ", " ") +".json"
#     with open(file_path,"r") as f:
#         data = json.load(f)
#         new_dic[uid_list[i].replace("\n", "")]={"cybertotal":data}
# # ner_token = {"HackOrg":"","OffAct":"","SamFile":"","SecTeam":"","Tool":"","Time":"","Purp":"","Area":"","Idus":"","Org":"","Way":"","Exp":"","Features":"","O":"","X":""}
# for i in range(0,len(uid_list)):
#     # print(new_dic[uid_list[i].replace("\n", "")]["cybertotal"])
#     tokens = bio_list[i].split()
#     str_token = str_list[i].split()
#     temp_pre = ""
#     temp_lst = ""
#     ner_token = {"HackOrg":"","OffAct":"","SamFile":"","SecTeam":"","Tool":"","Time":"","Purp":"","Area":"","Idus":"","Org":"","Way":"","Exp":"","Features":"","O":"","X":""}
#     B_c = 0
#     for t in range(0,len(tokens)):
#         if B_c == 1 and tokens[t].split("-")[0]!="B" and tokens[t] != "O" and tokens[t] != "X" and tokens[t] !="" and temp_pre!= "O" and temp_pre !="X":
#             ner_token[tokens[t].split("-")[1]] +=  " " + str_token[t].replace(",", "").replace(".", "")
#         elif tokens[t].split("-")[0]=="B" and tokens[t] !="":
#             B_c=1
#             ner_token[tokens[t].split("-")[1]] +=  "," + str_token[t].replace(",", "").replace(".", "")
#         elif tokens[t] == "X" or tokens[t] == "O":
#             B_c = 0
#         temp_pre = tokens[t].split("-")[0]
#     for k in ner_token:
#         if len(ner_token[k])>0:
#             ner_token[k]=ner_token[k][1:]
#     new_dic[uid_list[i].replace("\n", "")]["ner"] = ner_token
#     # print(new_dic[uid_list[i].replace(\"\\n\", \"\")])\n"

import pickle 
with open('saved_dictionary3.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

new_dic = {}
count = 0
for i in loaded_dict:
    # print(loaded_dict[i])
    if "gpt"  in loaded_dict[i].keys():
        new_dic[i] = loaded_dict[i]
        if "area_score" not in loaded_dict[i]["ner"].keys():
            new_dic[i]["ner"]["area_score"] = 0
        if "idus_score" not in loaded_dict[i]["ner"].keys():
            new_dic[i]["ner"]["idus_score"] = 0
        if "hackorg_score" not in loaded_dict[i]["ner"].keys():
            new_dic[i]["ner"]["hackorg_score"] = 0
        if "area_score" not in loaded_dict[i]["gpt"].keys():
            new_dic[i]["gpt"]["area_score"] = 0
        if "idus_score" not in loaded_dict[i]["gpt"].keys():
            new_dic[i]["gpt"]["idus_score"] = 0
        if "hackorg_score" not in loaded_dict[i]["gpt"].keys():
            new_dic[i]["gpt"]["hackorg_score"] = 0
        if new_dic[i]["ner"]["area_score"] != 0:
            count+=1

temp = ""
temp_index = "area_score"
print("目前比數有"+str(len(new_dic)))
print("目前評分完數量"+str(count))
app = Flask(__name__)

@app.route("/")
def hello():
    global temp_index
    temp_index = "area_score"
    key = random.choice(list(new_dic.keys()))
    # key = "5f6824e71ba44d0ab81dc8a653a6fd70"
    # while len(new_dic[key]["cybertotal"]["description"].split()) < 50:
    #     key = random.choice(list(new_dic.keys()))
    while not new_dic[key]["ner"]["Idus"] or new_dic[key]["ner"]["area_score"] == 0 :
        key = random.choice(list(new_dic.keys()))
    print(key)
    print(new_dic[key]['ner']["area_score"])
    print(new_dic[key]['ner']["idus_score"])
    print(new_dic[key]['ner']["hackorg_score"])
    print(new_dic[key]['gpt']["area_score"])
    print(new_dic[key]['gpt']["idus_score"])
    print(new_dic[key]['gpt']["hackorg_score"])
    return render_template("index.html",data=new_dic[key],temp_index = temp_index)



@app.route("/save_model",methods=["POST"])
def save_model():
    with open('saved_dictionary3.pkl', 'wb') as f:
        pickle.dump(new_dic, f)
    return  json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



@app.route("/update_index",methods=["POST"])
def update_index():
    global temp
    global temp_index
    temp = request.values["cn"]
    otx_id = request.values["otx_id"]
    if temp == "r3":
        temp_index = "area_score"
    elif temp == "r4":
        temp_index = "idus_score"
    elif temp == "r5":
        temp_index = "hackorg_score"
    men_index = "men_"+temp_index.split("_")[0] 
    if men_index not in new_dic[otx_id]["cybertotal"].keys():
        new_dic[otx_id]["cybertotal"][men_index] = 0
    if temp_index not in new_dic[otx_id]["ner"].keys():
        new_dic[otx_id]["ner"][temp_index] = 0
    if temp_index not in new_dic[otx_id]["gpt"].keys():
        new_dic[otx_id]["gpt"][temp_index] = 0
    if temp_index not in new_dic[otx_id]["bert"].keys():
        new_dic[otx_id]["bert"][temp_index] = 0
    c_t = new_dic[otx_id]["cybertotal"][men_index]
    print(men_index,c_t)
    g_t = new_dic[otx_id]["gpt"][temp_index]
    n_t = new_dic[otx_id]["ner"][temp_index]
    b_t = new_dic[otx_id]["bert"][temp_index]
    print(c_t,g_t,n_t,b_t)
    
    if c_t == 0:
        c_t = 0
    elif c_t == 1:
        print("sdsd")
        c_t = "cybertotal_men"
    elif c_t == 2:
        print("xcxcx")
        c_t = "cybertotal_not"
    if n_t == 0:
        n_t = 0
    elif n_t == 1:
        n_t = "ner_c"
    elif n_t == 2:
        n_t = "ner_e"
    elif n_t == 3:
        n_t = "ner_n"
    elif n_t == 4:
        n_t = "ner_m"
    if g_t == 0:
        g_t = 0
    elif g_t == 1:
        g_t = "gpt_c"
    elif g_t ==2:
        g_t = "gpt_e"
    elif g_t == 3:
        g_t = "gpt_n"
    elif g_t == 4:
        g_t = "gpt_m"
    if b_t == 0:
        b_t = 0
    elif b_t == 1:
        b_t = "bert_c"
    elif b_t ==2:
        b_t = "bert_e"
    elif b_t == 3:
        b_t = "bert_n"
    elif b_t == 4:
        b_t = "bert_m"
    print(c_t,n_t,g_t,b_t)
    return  json.dumps({'success':temp_index,'ner_score':n_t,'gpt_score':g_t,"men_score":c_t,"bert_score":b_t}), 200, {'ContentType':'application/json'}

@app.route("/update_men",methods=["POST"])
def update_men():
    ans = request.values["cn"]
    otx_id = request.values["otx_id"]
    ans_code = 0
    indexx = request.values["indexx"]
    print(indexx)
    try:
        if indexx == "0":
            temp_index = "men_area"
        elif indexx == "1":
            temp_index = "men_idus"
        elif indexx == "2":
            temp_index = "men_hackorg"
        if ans == "cybertotal_men": 
            ans_code = 1
        elif ans == "cybertotal_not":
            ans_code = 2
        print(temp_index,ans_code)
        new_dic[otx_id]["cybertotal"][temp_index]  = ans_code
        print(new_dic[otx_id]["cybertotal"][temp_index])
        return  json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as e:
        return json.dumps({'error':str(e)}), 500, {'ContentType':'application/json'}

@app.route("/update_bert",methods=["POST"])
def update_bert():
    ans = request.values["cn"]
    otx_id = request.values["otx_id"]
    ans_code = 0
    indexx = request.values["indexx"]
    print(indexx)
    try:
        if indexx == "0":
            temp_index = "area_score"
        elif indexx == "1":
            temp_index = "idus_score"
        elif indexx == "2":
            temp_index = "hackorg_score"
        if ans == "bert_c":
            ans_code = 1
        elif ans == "bert_e":
            ans_code = 2
        elif ans == "bert_n":
            ans_code = 3
        elif ans == "bert_m":
            ans_code = 4
        new_dic[otx_id]["bert"][temp_index] = ans_code
        print("update bert :"+str(new_dic[otx_id]["bert"][temp_index]))
        return  json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as e:
        return json.dumps({'error':str(e)}), 500, {'ContentType':'application/json'}

@app.route("/update_ner",methods=["POST"])
def update_ner():
    ans = request.values["cn"]
    otx_id = request.values["otx_id"]
    ans_code = 0
    indexx = request.values["indexx"]
    print(indexx)
    try:
        if indexx == "0":
            temp_index = "area_score"
        elif indexx == "1":
            temp_index = "idus_score"
        elif indexx == "2":
            temp_index = "hackorg_score"
        if ans == "ner_c":
            ans_code = 1
        elif ans == "ner_e":
            ans_code = 2
        elif ans == "ner_n":
            ans_code = 3
        elif ans == "ner_m":
            ans_code = 4
        new_dic[otx_id]["ner"][temp_index] = ans_code
        return  json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as e:
        return json.dumps({'error':str(e)}), 500, {'ContentType':'application/json'}

@app.route("/update_gpt",methods=["POST"])
def update_gpt():
    global temp_index
    ans = request.values["cn"]
    otx_id = request.values["otx_id"]
    ans_code = 0
    indexx = request.values["indexx"]
    try:
        if indexx == "0":
            temp_index = "area_score"
        elif indexx == "1":
            temp_index = "idus_score"
        elif indexx == "2":
            temp_index = "hackorg_score"
        if ans == "gpt_c":
            ans_code = 1
        elif ans == "gpt_e":
            ans_code = 2
        elif ans == "gpt_n":
            ans_code = 3
        elif ans == "gpt_m":
            ans_code = 4
        new_dic[otx_id]["gpt"][temp_index] = ans_code
        return  json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as e:
        return json.dumps({'error':str(e)}), 500, {'ContentType':'application/json'}    

if __name__ == "__main__":
    app.run(debug=True,port=8000)