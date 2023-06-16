from flask import Flask,request,jsonify
from flask_restful import Api, Resource
import requests
from scrapy import Selector
app=Flask(__name__)
api=Api(app)

headers={
'Authority':'www.amazon.in',
'Method':'GET',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Cookie':'session-id=261-0181003-5646351; session-id-time=2082787201l; i18n-prefs=INR; ubid-acbin=258-6304053-0307118; lc-acbin=en_IN; session-token=MFgs/hwQZc6jEASJNM3JhK3LAGDktTPjwPjG1adDiSQ+sSOvPgLcSsBpF296wYYocW+vuIp/8Qc5PNt3yuJe8SScRIrAerUsUm+0dVeuqElrlF+9V97F25B5yoDpyse2YChUmQtBWsMHZoq/MMx1Lc3f86HQVRx+cKLO16D4+vHzj8gaLxFZfZEpRJXP0jaYANiubk73FzS3DyaWGLeX9ctiQzwgPUKHZRZu7joBYio=; csm-hit=tb:XGY1VPD3P6Y277J885Y8+s-XGY1VPD3P6Y277J885Y8|1686120572884&t:1686120572884&adb:adblk_yes',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37',
}

class Aamzon(Resource):
    def get(self,asin):
        self.asin=asin
        link='https://www.amazon.in/dp/'+self.asin
        re=requests.get(url=link,headers=headers)
        if re.status_code==200:
            page_content=Selector(text=re.text)
            data_dict={}
            # Todo GET PRODUCT NAME
            try:
                prd_name=page_content.xpath('//h1/span/text()').get()
                data_dict['Product_Name']=prd_name.replace(' ','')
            except Exception as e:
                print(e)

            # Todo GET PRODUCT MARKDOWN PRICE
            try:
                mrk_price = page_content.xpath('//div[@id="apex_desktop"]//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//text()').get()
                if mrk_price == None:
                    mrk_price = page_content.xpath('//div[@id="apex_desktop"]//span[@class="a-price a-text-price"]//span//text()').get()
                    if mrk_price == None:
                        mrk_price = page_content.xpath('//div[@id="apex_desktop"]//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]//span//text()').get()
                if mrk_price:
                    nw_mrk_price = mrk_price.replace('"', '')
                else:
                    nw_mrk_price=None

                data_dict['Markdown_Price']=nw_mrk_price
            except Exception as e:
                print(e)

            # Todo GET PRODUCT REGULAR PRICE
            try:
                regu_price = page_content.xpath('//div[@id="apex_desktop"]//*[contains(text(),"M.R.P.:")]//span//span//text()').get()
                if regu_price == None:
                    regu_price = page_content.xpath('//div[@id="apex_desktop"]//*[contains(text(),"M.R.P.:")]//..//span[@class="a-price a-text-price a-size-base"]//span//text()').get()
                    if regu_price == None:
                        regu_price = page_content.xpath('//div[@id="apex_desktop"]//*[contains(text(),"M.R.P.:")]//span//span//text()').get()
                if regu_price:
                    nw_regu_price =regu_price.replace('"','')
                    print(nw_regu_price)
                else:
                    nw_regu_price = None

                data_dict['Regular_Price']=nw_regu_price
            except Exception as e:
                print(e)

            # Todo Seller Name
            try:
                seller_name=page_content.xpath('//div[@id="shipsFromSoldByInsideBuyBox_feature_div"]//*[contains(text(),"Sold by")]//..//a//span//text()').get()
                if seller_name:
                    seller_name=seller_name
                else:
                    seller_name=None

                data_dict['Seller_Name']=seller_name
            except Exception as e:
                print(e)

            return jsonify(data_dict)

        else:
            return {'Error':"PARAMETER ASIN IS WRONG PASS PLEASE CHECK"},404


api.add_resource(Aamzon,'/<string:asin>')

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)