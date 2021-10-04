from __future__ import unicode_literals

import json

from datetime import date
import locale
import frappe
import os
import re
import random
import string
import requests
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

@frappe.whitelist()
def get_tax_info(**args):
    bizno = args.get('bzno')
    dongCode= bizno[3:5]
    country_code = args.get('country_code')
    docname = args.get('docname')
    x = datetime.now()
    x_str = str(x)
    yyyymmdd = x_str[0:10]
    print(args)
    if country_code == "KR" or country_code == "kr":
        url = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
        request = urllib.request.Request(url)
        #request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("Accept", "application/xml; charset=UTF-8")
        request.add_header("Accept-Encoding", "gzip, deflate, br")
        request.add_header("Accept-Language", "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
        request.add_header("Connection", "keep-alive")
        request.add_header("Content-Length", "257")
        request.add_header("Content-Type", "application/xml; charset=UTF-8")
        request.add_header("Host", "teht.hometax.go.kr")
        request.add_header("Origin", "https://teht.hometax.go.kr")
        request.add_header("Referer", "https://teht.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/ab/a/a/UTEABAAA13.xml")
        request.add_header("Sec-Fetch-Mode", "cors")
        request.add_header("Sec-Fetch-Site", "same-origin")
        request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")

        CRLF = "\n"
        data=""
        data= "<map id=\"ATTABZAA001R08\">" + CRLF
        data+=" <pubcUserNo/>" + CRLF
        data+=" <mobYn>N</mobYn>" + CRLF
        data+=" <inqrTrgtClCd>1</inqrTrgtClCd>" + CRLF
        data+=" <txprDscmNo>" + bizno + "</txprDscmNo>" + CRLF
        data+=" <dongCode>" + dongCode + "</dongCode>" + CRLF
        data+=" <psbSearch>Y</psbSearch>" + CRLF
        data+=" <map id=\"userReqInfoVO\"/>" + CRLF
        data+="</map>" + CRLF

        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        print(docname)
        credit_check1 = frappe.get_doc('Credit Check',docname)


        if (rescode == 200):
            response_body = response.read().decode("utf-8")
            print(response_body)
            soup = BeautifulSoup(response_body, "xml")
            smpcbmantrtcntn = (soup.find_all(name="smpcBmanTrtCntn"))[0].text.strip()
            trtcntn = (soup.find_all(name="trtCntn"))[0].text.strip()
            nrgtTxprYn = (soup.find_all(name="nrgtTxprYn"))[0].text.strip()
            credit_check1.smpcbmantrtcntn = smpcbmantrtcntn
            credit_check1.trtcntn = trtcntn
            credit_check1.base_date = yyyymmdd
            credit_check1.bzno = bizno
            print(smpcbmantrtcntn+"\n"+trtcntn+"\n"+nrgtTxprYn)

    return credit_check1

@frappe.whitelist()
def get_company_info(**args):
    print(args)
    bzno = args.get('bzno')
    country_code = args.get('country_code')
    credit_check = frappe.new_doc('Credit Check')
    credit_check.bzno = bzno
    credit_check.country_cd = country_code
    secrets_file = os.path.join(os.getcwd(), 'secrets.json')
    with open(secrets_file) as f:
        secrets = json.load(f)

    if country_code == "KR" or country_code == "kr":
        url1 = secrets["credit_url"]
        data = {
            'user_id': secrets["credit_user_id"],
            'process': '',
            'ctz_bzer_cono': bzno,
            'ctz_bzer_cono_cls': '2',
            'jm_no': 'E015'
        }
        res1 = requests.post(url1, data=data)
        html = res1.content
        #print(html)
        soup = BeautifulSoup(html, "xml")
        try:
            error_code  = soup.find_all(name="err_cd")
            if  error_code[0].text.strip() == "00":

                enp_nm_list = soup.find_all(name="enp_nm")

                for enp_nm in enp_nm_list:
                    credit_check.enp_nm = enp_nm.text.strip()
                    enp_nm_trd = soup.find_all(name="enp_nm_trd")
                    credit_check.enp_nm_trd = enp_nm_trd[0].text.strip()
                    cono_pid = soup.find_all(name="cono_pid")
                    credit_check.cono_pid = cono_pid[0].text
                    eng_enp_nm = soup.find_all(name="eng_enp_nm")
                    credit_check.eng_enp_nm = eng_enp_nm[0].text.strip()
                    reper_nm = soup.find_all(name="reper_nm")
                    credit_check.reper_nm = reper_nm[0].text.strip()
                    estb_dt = soup.find_all(name="estb_dt")
                    credit_check.estb_dt = estb_dt[0].text
                    enp_fcd = soup.find_all(name="enp_fcd")
                    credit_check.enp_fcd = enp_fcd[0].text
                    ipo_cd = soup.find_all(name="ipo_cd")
                    credit_check.ipo_cd = ipo_cd[0].text
                    acct_mm = soup.find_all(name="acct_mm")
                    credit_check.acct_mm = acct_mm[0].text
                    group_nm = soup.find_all(name="group_nm")
                    credit_check.group_nm = group_nm[0].text
                    em_cnt = soup.find_all(name="em_cnt")
                    credit_check.em_cnt = em_cnt[0].text
                    bzc_cd = soup.find_all(name="bzc_cd")
                    credit_check.bzc_cd = bzc_cd[0].text
                    zip = soup.find_all(name="zip")
                    credit_check.zip = zip[0].text
                    addr1 = soup.find_all(name="addr1")
                    credit_check.addr1 = addr1[0].text
                    addr2 = soup.find_all(name="addr2")
                    credit_check.addr2 = addr2[0].text
                    tel_no = soup.find_all(name="tel_no")
                    credit_check.tel_no = tel_no[0].text
                    fax_no = soup.find_all(name="fax_no")
                    credit_check.fax_no = fax_no[0].text
                    major_pd = soup.find_all(name="major_pd")
                    credit_check.major_pd = major_pd[0].text
                    mtx_bnk_nm = soup.find_all(name="mtx_bnk_nm")
                    credit_check.mtx_bnk_nm = mtx_bnk_nm[0].text
                    enp_scd = soup.find_all(name="enp_scd")
                    credit_check.enp_scd = enp_scd[0].text
                    enp_scd_chg_dt = soup.find_all(name="enp_scd_chg_dt")
                    credit_check.enp_scd_chg_dt = enp_scd_chg_dt[0].text
                    enp_sze = soup.find_all(name="enp_sze")
                    credit_check.enp_sze = enp_sze[0].text
                    opnn_enp = soup.find_all(name="opnn_enp")
                    credit_check.opnn_enp = opnn_enp[0].text
                    opnn_sales = soup.find_all(name="opnn_sales")
                    credit_check.opnn_sales = opnn_sales[0].text
                    opnn_reper = soup.find_all(name="opnn_reper")
                    credit_check.opnn_reper = opnn_reper[0].text
                    cr_grd = soup.find_all(name="cr_grd")
                    credit_check.cr_grd = cr_grd[0].text
                    bzc_nm = soup.find_all(name="bzc_nm")
                    credit_check.bzc_nm = bzc_nm[0].text


                    cr_grd_dtl = soup.find_all(name="cr_grd_dtl")
                    credit_check.cr_grd_dtl = cr_grd_dtl[0].text
                    grd_cls = soup.find_all(name="grd_cls")
                    credit_check.grd_cls = grd_cls[0].text
                    evl_dt = soup.find_all(name="evl_dt")
                    credit_check.evl_dt = evl_dt[0].text
                    sttl_base_dt = soup.find_all(name="sttl_base_dt")
                    credit_check.sttl_base_dt = sttl_base_dt[0].text
                    kfb_bad_cnt = soup.find_all(name="kfb_bad_cnt")
                    credit_check.kfb_bad_cnt = kfb_bad_cnt[0].text
                    kfb_fin_tx_cnt = soup.find_all(name="kfb_fin_tx_cnt")
                    credit_check.kfb_fin_tx_cnt = kfb_fin_tx_cnt[0].text
                    workout_cnt = soup.find_all(name="workout_cnt")
                    credit_check.workout_cnt = workout_cnt[0].text
                    dshovd_cnt = soup.find_all(name="dshovd_cnt")
                    credit_check.dshovd_cnt = dshovd_cnt[0].text
                    kedcd = soup.find_all(name="kedcd")
                    credit_check.kedcd = kedcd[0].text

                    customer_nm1 = soup.find_all(name="customer_nm1")
                    credit_check.customer_nm1 = customer_nm1[0].text
                    customer_nm2 = soup.find_all(name="customer_nm2")
                    credit_check.customer_nm2 = customer_nm2[0].text
                    customer_nm3 = soup.find_all(name="customer_nm3")
                    credit_check.customer_nm3 = customer_nm3[0].text

                    customer_rt1 = soup.find_all(name="customer_rt1")
                    credit_check.customer_rt1 = customer_rt1[0].text
                    customer_rt2 = soup.find_all(name="customer_rt2")
                    credit_check.customer_rt2 = customer_rt2[0].text
                    customer_rt3 = soup.find_all(name="customer_rt3")
                    credit_check.customer_rt3 = customer_rt3[0].text

                    supplier_nm1 = soup.find_all(name="supplier_nm1")
                    credit_check.supplier_nm1 = supplier_nm1[0].text
                    supplier_nm2 = soup.find_all(name="supplier_nm2")
                    credit_check.supplier_nm2 = supplier_nm2[0].text
                    supplier_nm3 = soup.find_all(name="supplier_nm3")
                    credit_check.supplier_nm3 = supplier_nm3[0].text

                    supplier_rt1 = soup.find_all(name="supplier_rt1")
                    credit_check.supplier_rt1 = supplier_rt1[0].text
                    supplier_rt2 = soup.find_all(name="supplier_rt2")
                    credit_check.supplier_rt2 = supplier_rt2[0].text
                    supplier_rt3 = soup.find_all(name="supplier_rt3")
                    credit_check.supplier_rt3 = supplier_rt3[0].text
        except IndexError:
            print("Exception error")


#    print(credit_check)
    return credit_check


@frappe.whitelist()
def get_company_info_batch(**args):
    customer_list  = frappe.db.get_list('Customer', fields=['tax_id','name'])
    print(args)
    print(customer_list)
    secrets_file = os.path.join(os.getcwd(), 'secrets.json')
    with open(secrets_file) as f:
        secrets = json.load(f)

    for tax_id0 in customer_list:
        tax_id1 = re.sub("\-", "", tax_id0.tax_id)
        print(tax_id0.name)
        ex_exists = frappe.db.exists({
            'doctype': 'Credit Check',
            'name': "KR-"+tax_id1

        })
        if not ex_exists:
            credit_check = frappe.new_doc('Credit Check')
            credit_check.bzno = tax_id1
            credit_check.country_cd = "kr"
            credit_check.name =  "KR-"+tax_id1

            if len(tax_id1)  == 10 :
                url1 = secrets["credit_url"]
                data = {
                    'user_id': secrets["credit_user_id"],
                    'process': '',
                    'ctz_bzer_cono': tax_id1,
                    'ctz_bzer_cono_cls': '2',
                    'jm_no': 'E015'
                }
                res1 = requests.post(url1, data=data)
                html = res1.content
                # print(html)
                soup = BeautifulSoup(html, "xml")
                try:
                    error_code = soup.find_all(name="err_cd")
                    if error_code[0].text.strip() == "00":

                        enp_nm_list = soup.find_all(name="enp_nm")

                        for enp_nm in enp_nm_list:
                            credit_check.enp_nm = enp_nm.text.strip()
                            enp_nm_trd = soup.find_all(name="enp_nm_trd")
                            credit_check.enp_nm_trd = enp_nm_trd[0].text.strip()
                            cono_pid = soup.find_all(name="cono_pid")
                            credit_check.cono_pid = cono_pid[0].text
                            eng_enp_nm = soup.find_all(name="eng_enp_nm")
                            credit_check.eng_enp_nm = eng_enp_nm[0].text.strip()
                            reper_nm = soup.find_all(name="reper_nm")
                            credit_check.reper_nm = reper_nm[0].text.strip()
                            estb_dt = soup.find_all(name="estb_dt")
                            credit_check.estb_dt = estb_dt[0].text
                            enp_fcd = soup.find_all(name="enp_fcd")
                            credit_check.enp_fcd = enp_fcd[0].text
                            ipo_cd = soup.find_all(name="ipo_cd")
                            credit_check.ipo_cd = ipo_cd[0].text
                            acct_mm = soup.find_all(name="acct_mm")
                            credit_check.acct_mm = acct_mm[0].text
                            group_nm = soup.find_all(name="group_nm")
                            credit_check.group_nm = group_nm[0].text
                            em_cnt = soup.find_all(name="em_cnt")
                            credit_check.em_cnt = em_cnt[0].text
                            bzc_cd = soup.find_all(name="bzc_cd")
                            credit_check.bzc_cd = bzc_cd[0].text
                            zip = soup.find_all(name="zip")
                            credit_check.zip = zip[0].text
                            addr1 = soup.find_all(name="addr1")
                            credit_check.addr1 = addr1[0].text
                            addr2 = soup.find_all(name="addr2")
                            credit_check.addr2 = addr2[0].text
                            tel_no = soup.find_all(name="tel_no")
                            credit_check.tel_no = tel_no[0].text
                            fax_no = soup.find_all(name="fax_no")
                            credit_check.fax_no = fax_no[0].text
                            major_pd = soup.find_all(name="major_pd")
                            credit_check.major_pd = major_pd[0].text
                            mtx_bnk_nm = soup.find_all(name="mtx_bnk_nm")
                            credit_check.mtx_bnk_nm = mtx_bnk_nm[0].text
                            enp_scd = soup.find_all(name="enp_scd")
                            credit_check.enp_scd = enp_scd[0].text
                            enp_scd_chg_dt = soup.find_all(name="enp_scd_chg_dt")
                            credit_check.enp_scd_chg_dt = enp_scd_chg_dt[0].text
                            enp_sze = soup.find_all(name="enp_sze")
                            credit_check.enp_sze = enp_sze[0].text
                            opnn_enp = soup.find_all(name="opnn_enp")
                            credit_check.opnn_enp = opnn_enp[0].text
                            opnn_sales = soup.find_all(name="opnn_sales")
                            credit_check.opnn_sales = opnn_sales[0].text
                            opnn_reper = soup.find_all(name="opnn_reper")
                            credit_check.opnn_reper = opnn_reper[0].text
                            cr_grd = soup.find_all(name="cr_grd")
                            credit_check.cr_grd = cr_grd[0].text
                            bzc_nm = soup.find_all(name="bzc_nm")
                            credit_check.bzc_nm = bzc_nm[0].text

                            cr_grd_dtl = soup.find_all(name="cr_grd_dtl")
                            credit_check.cr_grd_dtl = cr_grd_dtl[0].text
                            grd_cls = soup.find_all(name="grd_cls")
                            credit_check.grd_cls = grd_cls[0].text
                            evl_dt = soup.find_all(name="evl_dt")
                            credit_check.evl_dt = evl_dt[0].text
                            sttl_base_dt = soup.find_all(name="sttl_base_dt")
                            credit_check.sttl_base_dt = sttl_base_dt[0].text
                            kfb_bad_cnt = soup.find_all(name="kfb_bad_cnt")
                            credit_check.kfb_bad_cnt = kfb_bad_cnt[0].text
                            kfb_fin_tx_cnt = soup.find_all(name="kfb_fin_tx_cnt")
                            credit_check.kfb_fin_tx_cnt = kfb_fin_tx_cnt[0].text
                            workout_cnt = soup.find_all(name="workout_cnt")
                            credit_check.workout_cnt = workout_cnt[0].text
                            dshovd_cnt = soup.find_all(name="dshovd_cnt")
                            credit_check.dshovd_cnt = dshovd_cnt[0].text
                            kedcd = soup.find_all(name="kedcd")
                            credit_check.kedcd = kedcd[0].text

                            customer_nm1 = soup.find_all(name="customer_nm1")
                            credit_check.customer_nm1 = customer_nm1[0].text
                            customer_nm2 = soup.find_all(name="customer_nm2")
                            credit_check.customer_nm2 = customer_nm2[0].text
                            customer_nm3 = soup.find_all(name="customer_nm3")
                            credit_check.customer_nm3 = customer_nm3[0].text

                            customer_rt1 = soup.find_all(name="customer_rt1")
                            credit_check.customer_rt1 = customer_rt1[0].text
                            customer_rt2 = soup.find_all(name="customer_rt2")
                            credit_check.customer_rt2 = customer_rt2[0].text
                            customer_rt3 = soup.find_all(name="customer_rt3")
                            credit_check.customer_rt3 = customer_rt3[0].text

                            supplier_nm1 = soup.find_all(name="supplier_nm1")
                            credit_check.supplier_nm1 = supplier_nm1[0].text
                            supplier_nm2 = soup.find_all(name="supplier_nm2")
                            credit_check.supplier_nm2 = supplier_nm2[0].text
                            supplier_nm3 = soup.find_all(name="supplier_nm3")
                            credit_check.supplier_nm3 = supplier_nm3[0].text

                            supplier_rt1 = soup.find_all(name="supplier_rt1")
                            credit_check.supplier_rt1 = supplier_rt1[0].text
                            supplier_rt2 = soup.find_all(name="supplier_rt2")
                            credit_check.supplier_rt2 = supplier_rt2[0].text
                            supplier_rt3 = soup.find_all(name="supplier_rt3")
                            credit_check.supplier_rt3 = supplier_rt3[0].text
                        credit_check.insert()
                        frappe.db.set_value('Customer', tax_id0.name, {
                            'credit_check': "KR-"+tax_id1 ,
                            'customer_name' :  enp_nm_trd
                        })

                except IndexError:
                    print("Exception error")
            print(tax_id1)

    return True
@frappe.whitelist()
def get_tax_info_batch(**args):
    credit_check_list = frappe.db.get_list('Credit Check', fields=['name', 'bzno'])

    x = datetime.now()
    x_str = str(x)
    yyyymmdd = x_str[0:10]

    for credit_check1  in credit_check_list:
        bizno = credit_check1.bzno
        dongCode = bizno[3:5]
        url = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/xml; charset=UTF-8")
        request.add_header("Accept-Encoding", "gzip, deflate, br")
        request.add_header("Accept-Language", "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
        request.add_header("Connection", "keep-alive")
        request.add_header("Content-Length", "257")
        request.add_header("Content-Type", "application/xml; charset=UTF-8")
        request.add_header("Host", "teht.hometax.go.kr")
        request.add_header("Origin", "https://teht.hometax.go.kr")
        request.add_header("Referer", "https://teht.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/ab/a/a/UTEABAAA13.xml")
        request.add_header("Sec-Fetch-Mode", "cors")
        request.add_header("Sec-Fetch-Site", "same-origin")
        request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")

        CRLF = "\n"
        data=""
        data= "<map id=\"ATTABZAA001R08\">" + CRLF
        data+=" <pubcUserNo/>" + CRLF
        data+=" <mobYn>N</mobYn>" + CRLF
        data+=" <inqrTrgtClCd>1</inqrTrgtClCd>" + CRLF
        data+=" <txprDscmNo>" + bizno + "</txprDscmNo>" + CRLF
        data+=" <dongCode>" + dongCode + "</dongCode>" + CRLF
        data+=" <psbSearch>Y</psbSearch>" + CRLF
        data+=" <map id=\"userReqInfoVO\"/>" + CRLF
        data+="</map>" + CRLF

        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()



        if (rescode == 200):
            response_body = response.read().decode("utf-8")
            print(response_body)
            soup = BeautifulSoup(response_body, "xml")
            smpcbmantrtcntn = (soup.find_all(name="smpcBmanTrtCntn"))[0].text.strip()
            trtcntn = (soup.find_all(name="trtCntn"))[0].text.strip()
            nrgtTxprYn = (soup.find_all(name="nrgtTxprYn"))[0].text.strip()

            frappe.db.set_value('Credit Check', credit_check1.name, {
                'smpcbmantrtcntn': smpcbmantrtcntn,
                'trtcntn': trtcntn,
                'base_date': yyyymmdd
            })

            customer_tax = frappe.db.get_value('Customer', {'credit_check': credit_check1.name}, 'name')
            frappe.db.set_value('Customer', customer_tax, 'home_tax_msg', smpcbmantrtcntn)

            print(smpcbmantrtcntn+"\n"+trtcntn+"\n"+nrgtTxprYn)

    return True
