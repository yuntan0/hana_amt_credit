// Copyright (c) 2021, PJS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Credit Check', {
	refresh: function(frm) {
        frm.add_custom_button(__('Credit Check'),function(){
            //frappe.msgprint(frm.doc.date);
            let bzno = frm.selected_doc.bzno.replaceAll("-","");;
            let country_code = frm.selected_doc.country_code.toUpperCase();
            //frappe.msgprint(country_code);

            var me = this;

            frappe.call({
				method: "hana_amt_credit.hana_amt_credit.doctype.credit_check.api.get_company_info", //dotted path to server method
				args: {
					'country_code':country_code,
					'bzno':bzno
				},

				callback: function(r) {

					console.log(r)
					//cur_frm.exchange_rate = r.message.exchange_rate;
					if(r.message) {
						// code snippet
						//frappe.msgprint();
						//frappe.msgprint({
						//	title: __('Exchange rate created'),
						//	message: __('Check exchange rate')+r.message.exchange_rate,
						//	indicator: 'orange'
						//});
						//frm.selected_doc.exchange_rate = r.message.exchange_rate;
						cur_frm.set_value('bzno',r.message.bzno);
						cur_frm.set_value('enp_nm',r.message.enp_nm);
						cur_frm.set_value('addr1',r.message.addr1);
						cur_frm.set_value('addr2',r.message.addr2);
						cur_frm.set_value('bzc_cd',r.message.bzc_cd);
						cur_frm.set_value('em_cnt',r.message.em_cnt);
						cur_frm.set_value('eng_enp_nm',r.message.eng_enp_nm);
						cur_frm.set_value('enp_nm_trd',r.message.enp_nm_trd);
						cur_frm.set_value('enp_scd',r.message.enp_scd);
						cur_frm.set_value('enp_sze',r.message.enp_sze);
						cur_frm.set_value('estb_dt',r.message.estb_dt);
						cur_frm.set_value('enp_nm',r.message.enp_nm);
						cur_frm.set_value('fax_no',r.message.fax_no);
						cur_frm.set_value('group_nm',r.message.group_nm);
						cur_frm.set_value('major_pd',r.message.major_pd);
						cur_frm.set_value('mtx_bnk_nm',r.message.mtx_bnk_nm);
						cur_frm.set_value('reper_nm',r.message.reper_nm);
						cur_frm.set_value('tel_no',r.message.tel_no);
						cur_frm.set_value('zip',r.message.zip);

						cur_frm.set_value('opnn_enp',r.message.opnn_enp);
						cur_frm.set_value('opnn_sales',r.message.opnn_sales);
						cur_frm.set_value('opnn_reper',r.message.opnn_reper);
						cur_frm.set_value('cono_pid',r.message.cono_pid);

						cur_frm.set_value('cr_grd',r.message.cr_grd);
						cur_frm.set_value('bzc_nm',r.message.bzc_nm);

						cur_frm.set_value('cr_grd_dtl',r.message.cr_grd_dtl);
						cur_frm.set_value('grd_cls',r.message.grd_cls);
						cur_frm.set_value('evl_dt',r.message.evl_dt);
						cur_frm.set_value('sttl_base_dt',r.message.sttl_base_dt);
						cur_frm.set_value('kfb_bad_cnt',r.message.kfb_bad_cnt);
						cur_frm.set_value('kfb_fin_tx_cnt',r.message.kfb_fin_tx_cnt);
						cur_frm.set_value('workout_cnt',r.message.workout_cnt);
						cur_frm.set_value('dshovd_cnt',r.message.dshovd_cnt);
						cur_frm.set_value('kedcd',r.message.kedcd);

						cur_frm.set_value('customer_nm1',r.message.customer_nm1);
						cur_frm.set_value('customer_nm2',r.message.customer_nm2);
						cur_frm.set_value('customer_nm3',r.message.customer_nm3);

						cur_frm.set_value('customer_rt1',r.message.customer_rt1);
						cur_frm.set_value('customer_rt2',r.message.customer_rt2);
						cur_frm.set_value('customer_rt3',r.message.customer_rt3);

						cur_frm.set_value('supplier_nm1',r.message.supplier_nm1);
						cur_frm.set_value('supplier_nm2',r.message.supplier_nm2);
						cur_frm.set_value('supplier_nm3',r.message.supplier_nm3);

						cur_frm.set_value('supplier_rt1',r.message.supplier_rt1);
						cur_frm.set_value('supplier_rt2',r.message.supplier_rt2);
						cur_frm.set_value('supplier_rt3',r.message.supplier_rt3);


						return;
						//cur_frm.set_value('exchange_rate',r.message.exchange_rate);
						//cur_frm.exchange_rate = r.message.exchange_rate;

						}
				}
			})
        }, __("Get Company info")    );

        frm.add_custom_button(__('Credit Chech Batch'),function(){
            //frappe.msgprint(frm.doc.date);
            //let bzno = frm.selected_doc.bzno.replaceAll("-","");
            //let country_code = frm.selected_doc.country_code.toUpperCase();
            let docname = frm.selected_doc.name;
            //frappe.msgprint(country_code);

            var me = this;

            frappe.call({
				method: "hana_amt_credit.hana_amt_credit.doctype.credit_check.api.get_company_info_batch", //dotted path to server method
				args: {
					'docname':docname
				},

				callback: function(r) {

						console.log(r)
						// code snippet
						frappe.msgprint({
							title: __('Credit check created'),
							message: __('Credit check created'),
							indicator: 'orange'
						});


					}
			})
        }, __("Get Company info")    );

        frm.add_custom_button(__('Tax info'),function(){
            //frappe.msgprint(frm.doc.date);
            let bzno = frm.selected_doc.bzno.replaceAll("-","");
            let country_code = frm.selected_doc.country_code.toUpperCase();
            let docname = frm.selected_doc.name;
            //frappe.msgprint(country_code);

            var me = this;

            frappe.call({
				method: "hana_amt_credit.hana_amt_credit.doctype.credit_check.api.get_hometax_info", //dotted path to server method
				args: {
					'country_code':country_code,
					'bzno':bzno,
					'docname':docname
				},

				callback: function(r) {

					console.log(r)

					if(r.message) {
						// code snippet
						//frappe.msgprint();
						//frappe.msgprint({
						//	title: __('Exchange rate created'),
						//	message: __('Check exchange rate')+r.message.exchange_rate,
						//	indicator: 'orange'
						//});
						//frm.selected_doc.exchange_rate = r.message.exchange_rate;

						cur_frm.set_value('smpcbmantrtcntn',r.message.home_tax_msg);
						cur_frm.set_value('bzno',r.message.tax_id);
						cur_frm.set_value('trtcntn',r.message.taxation_type);
						cur_frm.set_value('base_date',r.message.home_tax_date);


						return;
						//cur_frm.set_value('exchange_rate',r.message.exchange_rate);
						//cur_frm.exchange_rate = r.message.exchange_rate;

						}
				}
			})
        }, __("Get Company info")    );


        frm.add_custom_button(__('Tax info Batch'),function(){
            //frappe.msgprint(frm.doc.date);
            let bzno = frm.selected_doc.bzno.replaceAll("-","");
            let country_code = frm.selected_doc.country_code.toUpperCase();
            let docname = frm.selected_doc.name;
            //frappe.msgprint(country_code);

            var me = this;

            frappe.call({
				method: "hana_amt_credit.hana_amt_credit.doctype.credit_check.api.get_tax_info_batch", //dotted path to server method
				args: {
					'docname':docname
				},

				callback: function(r) {

						console.log(r)
						// code snippet
						frappe.msgprint({
							title: __('Tax Info created'),
							message: __('Tax Info created'),
							indicator: 'orange'
						});


				}
			})
        }, __("Get Company info")    );

     }
});
