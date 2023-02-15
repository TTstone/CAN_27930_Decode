# 2022.11 xiehong@dfmc.com.cn
# 2023.2.1 更新：处理不完整的分段数据
# 2023.2.15 增加电芯最高电压
# 输出报文第一次出现时间以及具体的充电记录
import re #正则表达式
input_path = input("请输入文件名或者文件位置:")
with open(input_path, 'rt',encoding='utf-8') as f:
    data = f.read()
out_SPN = input_path+"关键报文时间节点.csv"
out_path = input_path+"交互数据.csv"
try:
    i_CHM = data.index('1826f456x CHM_CHG')
    CHM_time = data[i_CHM-27:i_CHM-20]
    def SPN_time_track(SPN):
        try:
            i_SPN = data.index(SPN)
            SPN_time = str(float(data[i_SPN-27:i_SPN-20]) - float(CHM_time))
        except:
            SPN_time = 'Null'
        return SPN_time
    #输出交互数据    
    with open(out_path, 'w') as f:
        f.write("Time_since_CHM,U_Req,I_Req,U_CCS,I_CCS,U_BCS,I_BCS,Min_T[C],Max_T[C],SOC,Ucell_max,Time_Charged[min]")
        f.write("\n")
        i = -1
        j_1 = data.rfind("1ceb56f4x dt")
        j_4= data.rfind('181056f4x BCL_BCU')
        j_3 = data.rfind("181356f4x BSM_BCU") 
        j_5 = data.rfind('1812f456x CCS_CHG')
        j_2 = data.rfind("cts                              0 0 8  8 11 02 01 ff ff 00 11 00")
        j = min(j_1,j_2,j_3,j_4,j_5)
        
        while i < j:
            start = i + 1
            i_1 = data.index('1ceb56f4x dt', start)
            i_2 = data.index('181056f4x BCL_BCU', start)
            i_3 = data.index('1812f456x CCS_CHG', start)
            i_4 = data.index('181356f4x BSM_BCU', start)
            i_5 = data.index('cts                              0 0 8  8 11 02 01 ff ff 00 11 00', start)
            i = min(i_1,i_2,i_3,i_4,i_5)
            i_time = data.index(' CANFD   1 Rx', i)
            i_BCS_Loop = data.index('1ceb56f4x dt', i)
            i_CCS_i = data.index('1812f456x CCS_CHG', i)
            i_reqUI = data.index('181056f4x BCL_BCU', i)
            i_maxT = data.index('181356f4x BSM_BCU', i) 
            result_time = str(float(data[i_time-11:i_time-4]) - float(data[i_CHM-27:i_CHM-20]))
            V_req = str(int((data[i_reqUI+55:i_reqUI+57] + data[i_reqUI+52:i_reqUI+54]), 16) * 0.1 + 0)
            I_req = str(-1 * (int((data[i_reqUI+61:i_reqUI+63] + data[i_reqUI+58:i_reqUI+60]), 16) * 0.1 - 400))
            V_CCS = str(int((data[i_CCS_i+55:i_CCS_i+57] + data[i_CCS_i+52:i_CCS_i+54]), 16) * 0.1 + 0)
            I_CCS = str(-1 * (int((data[i_CCS_i+61:i_CCS_i+63] + data[i_CCS_i+58:i_CCS_i+60]), 16) * 0.1 - 400))
            Time_charged = str(int(data[i_CCS_i+64:i_CCS_i+66],16))
            V_BCS = str(int((data[i_BCS_Loop+58:i_BCS_Loop+60] + data[i_BCS_Loop+55:i_BCS_Loop+57]),16) * 0.1 + 0)
            I_BCS = str(-1 * (int((data[i_BCS_Loop+64:i_BCS_Loop+66] + data[i_BCS_Loop+61:i_BCS_Loop+63]),16) * 0.1 -400))
            SOC = str(int(data[i_BCS_Loop+73:i_BCS_Loop+75],16))
            Ucell_max = str(int(data[i_BCS_Loop+71:i_BCS_Loop+72] + data[i_BCS_Loop+67:i_BCS_Loop+69],16) * 0.01)
            result_MaxT = int((data[i_maxT+55:i_maxT+57]),16)
            result_MaxT = str(result_MaxT -50)
            result_minT = int((data[i_maxT+61:i_maxT+63]),16)
            result_minT = str(result_minT -50)
            f.write(result_time)
            f.write(',')
            f.write(V_req)
            f.write(',')
            f.write(I_req)
            f.write(',')
            f.write(V_CCS)
            f.write(',')
            f.write(I_CCS)
            f.write(',')
            f.write(V_BCS)
            f.write(',')
            f.write(I_BCS)
            f.write(',')
            f.write(result_minT)
            f.write(',')
            f.write(result_MaxT)
            f.write(',')
            f.write(SOC)
            f.write(',')
            f.write(Ucell_max)
            f.write(',')
            f.write(Time_charged)
            f.write('\n')
    #输出报文时间节点
    with open(out_SPN, 'w') as f:
        time_absolute = data[0:35]
        f.write(time_absolute)
        f.write("\n")
        f.write('CHM_Time,')
        f.write('0')
        f.write("\n")
        BHM_time = SPN_time_track('182756f4x BHM_BCU')
        f.write('BHM_Time,')
        f.write(str(BHM_time))
        f.write("\n")
        CRM_time = SPN_time_track('1801f456x CRM_CHG')
        f.write('CRM_Time,')
        f.write(str(CRM_time))
        f.write("\n")
        i_BRM = re.search(r'1cecf456x cts[\s\S]{54}00 02 00', data, re.M).span()[0]
        BRM_time = str(float(data[i_BRM-27:i_BRM-20]) - float(CHM_time))
        f.write('BRM_Time,')
        f.write(str(BRM_time))
        f.write("\n")
        i_BCP = re.search(r'1cec56f4x rts[\s\S]{54}00 06 00', data, re.M).span()[0]
        BCP_time = str(float(data[i_BCP-27:i_BCP-20]) - float(CHM_time))
        f.write('BCP_Time,')
        f.write(str(BCP_time))
        f.write("\n")
        CML_time = SPN_time_track('1808f456x CML_CHG')
        f.write('CML_Time,')
        f.write(str(CML_time))
        f.write("\n")
        CTS_time = SPN_time_track('1807f456x CTS_CHG')
        f.write('CTS_Time,')
        f.write(str(CTS_time))
        f.write("\n")
        BRO_time = SPN_time_track('100956f4x BRO_BCU                          0 0 1  1 aa')
        f.write('BRO_Time,')
        f.write(str(BRO_time))
        f.write("\n")
        CRO_time = SPN_time_track('100af456x CRO_CHG                          0 0 1  1 aa')
        f.write('CRO_Time,')
        f.write(str(CRO_time))
        f.write("\n")
        BCL_time = SPN_time_track('181056f4x BCL_BCU')
        f.write('BCL_Time,')
        f.write(str(BCL_time))
        f.write("\n")
        BSM_time = SPN_time_track('181356f4x BSM_BCU')
        f.write('BSM_Time,')
        f.write(str(BSM_time))
        f.write("\n")
        i_BCS = re.search(r'1cec56f4x rts[\s\S]{54}00 11 00', data, re.M).span()[0]
        BCS_time = str(float(data[i_BCS-27:i_BCS-20]) - float(CHM_time))
        f.write('BCS_Time,')
        f.write(str(BCS_time))
        f.write("\n")
        CCS_time = SPN_time_track('1812f456x CCS_CHG')
        f.write('CCS_Time,')
        f.write(str(CCS_time))
        f.write("\n")
        CST_time = SPN_time_track('101af456x CST_CHG')
        f.write('CST_Time,')
        f.write(str(CST_time))
        f.write("\n")
        BST_time = SPN_time_track('101956f4x BST_BCU')
        f.write('BST_Time,')
        f.write(str(BST_time))
        f.write("\n")
        BSD_time = SPN_time_track('181c56f4x BSD_BCU')
        f.write('BSD_Time,')
        f.write(str(BSD_time))
        f.write("\n")
        CSD_time = SPN_time_track('181df456x CSD_CHG')
        f.write('CSD_Time,')
        f.write(str(CSD_time))
        f.write("\n")
except:
    i_CHM = data.index(' CANFD   1 Rx')
    CHM_time = float(data[i_CHM-11:i_CHM-4])
    print("报文数据不完整，只输出交互数据，不输出完整报文节点。时间起始点取当段数据的第一条报文")
    #不完整，只输出交互数据
    with open(out_path, 'w') as f:
        f.write("Time_since_CHM,U_Req,I_Req,U_CCS,I_CCS,U_BCS,I_BCS,Min_T[C],Max_T[C],SOC,Ucell_max,Time_Charged[min]")
        f.write("\n")
        i = -1
        j_1 = data.rfind("1ceb56f4x dt")
        j_4= data.rfind('181056f4x BCL_BCU')
        j_3 = data.rfind("181356f4x BSM_BCU") 
        j_5 = data.rfind('1812f456x CCS_CHG')
        j_2 = data.rfind("cts                              0 0 8  8 11 02 01 ff ff 00 11 00")
        j = min(j_1,j_2,j_3,j_4,j_5)
        
        while i < j:
            start = i + 1
            i_1 = data.index('1ceb56f4x dt', start)
            i_2 = data.index('181056f4x BCL_BCU', start)
            i_3 = data.index('1812f456x CCS_CHG', start)
            i_4 = data.index('181356f4x BSM_BCU', start)
            i_5 = data.index('cts                              0 0 8  8 11 02 01 ff ff 00 11 00', start)
            i = min(i_1,i_2,i_3,i_4,i_5)
            i_time = data.index(' CANFD   1 Rx', i)
            i_BCS_Loop = data.index('1ceb56f4x dt', i)
            i_CCS_i = data.index('1812f456x CCS_CHG', i)
            i_reqUI = data.index('181056f4x BCL_BCU', i)
            i_maxT = data.index('181356f4x BSM_BCU', i) 
            result_time = str(float(data[i_time-11:i_time-4]))
            V_req = str(int((data[i_reqUI+55:i_reqUI+57] + data[i_reqUI+52:i_reqUI+54]), 16) * 0.1 + 0)
            I_req = str(-1 * (int((data[i_reqUI+61:i_reqUI+63] + data[i_reqUI+58:i_reqUI+60]), 16) * 0.1 - 400))
            V_CCS = str(int((data[i_CCS_i+55:i_CCS_i+57] + data[i_CCS_i+52:i_CCS_i+54]), 16) * 0.1 + 0)
            I_CCS = str(-1 * (int((data[i_CCS_i+61:i_CCS_i+63] + data[i_CCS_i+58:i_CCS_i+60]), 16) * 0.1 - 400))
            Time_charged = str(int(data[i_CCS_i+64:i_CCS_i+66],16))
            V_BCS = str(int((data[i_BCS_Loop+58:i_BCS_Loop+60] + data[i_BCS_Loop+55:i_BCS_Loop+57]),16) * 0.1 + 0)
            I_BCS = str(-1 * (int((data[i_BCS_Loop+64:i_BCS_Loop+66] + data[i_BCS_Loop+61:i_BCS_Loop+63]),16) * 0.1 -400))
            SOC = str(int(data[i_BCS_Loop+73:i_BCS_Loop+75],16))
            Ucell_max = str(int(data[i_BCS_Loop+71:i_BCS_Loop+72] + data[i_BCS_Loop+67:i_BCS_Loop+69],16) * 0.01)
            result_MaxT = int((data[i_maxT+55:i_maxT+57]),16)
            result_MaxT = str(result_MaxT -50)
            result_minT = int((data[i_maxT+61:i_maxT+63]),16)
            result_minT = str(result_minT -50)
            f.write(result_time)
            f.write(',')
            f.write(V_req)
            f.write(',')
            f.write(I_req)
            f.write(',')
            f.write(V_CCS)
            f.write(',')
            f.write(I_CCS)
            f.write(',')
            f.write(V_BCS)
            f.write(',')
            f.write(I_BCS)
            f.write(',')
            f.write(result_minT)
            f.write(',')
            f.write(result_MaxT)
            f.write(',')
            f.write(SOC)
            f.write(',')
            f.write(Ucell_max)
            f.write(',')
            f.write(Time_charged)
            f.write('\n')
print("输出文件已经保存在原始文件目录")