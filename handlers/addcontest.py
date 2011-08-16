# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

import os, re
import conf
import logging
from model import Contest
from common import get_user, moderator
from datetime import datetime
from datetime import date, timedelta, datetime
from conf import DEBUG
from google.appengine.api import urlfetch


class AddContest( webapp.RequestHandler ):
   
    user, login_url, logout_url, username = None, None, None, None 
   
    
    def get_date( self, day, time ):
        
        # parsing it from the string
        pattern = r"""
            (\d+).(\d+).(\d+)    # day, month, year
            """
        reg = re.compile( pattern, re.VERBOSE )
        match = reg.search( day )
        d, m, y = int( match.group(1) ), int( match.group(2) ), int( match.group(3) )

        pattern = r"""
            (\d+):(\d+)         # hour, minute
            """
        reg = re.compile( pattern, re.VERBOSE )
        match = reg.search( time )
        hh, mm = int( match.group(1) ), int( match.group(2) )
        
        # creating the datetime object
        date = datetime( y, m, d, hh, mm )

        # taking offset +3h to make it bangladeshi time
        date = date + timedelta( hours=3 ) 
        return date

    
    def get_detail( self, date ):
        return date.strftime("%B %d, %Y - %A")  # August 15, 2011 - Monday  
    
    def get_time( self,  date ):
        return date.strftime("%I:%M%p")  # 04:30PM

    def load_contests(self):
       
        # cleaning up the previous data
        q = db.Query( Contest )
        contests = q.fetch( 1000 )
        db.delete( contests )
        
        # we won't pick the russian contests
        russia = [ 'contests.snarknews.info' , 'dl.gsu.by' ]  
        
        # fetching the contest events

        if DEBUG:
            f = r"""
    
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>

<head>
 <title>Contests list</title>
 <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
 <link rel="stylesheet" href="http://fs13.net/events/styles.css" type="text/css"> 
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-6591789-1");
pageTracker._trackPageview();
} catch(err) {}</script>
</head>

<body>

 <p>

 <div style='width:100%; text-align:center;'>
 <table border='1' cellpadding='3' cellspacing='0' style='width:100%'>
  <tr class='table_head'> 
   <td>
    Дата
   </td>
   <td >  
    Время
   </td>

   <td>
    Событие
   </td>
   <td>
    Ссылка
   </td>
  </tr>

  
	   <tr class='CurrentContest'> 
	   <td style='color: rgb(63, 63, 63);'>
	    16.08.2011 
	   </td>

	   <td style='color: rgb(63, 63, 63);'> 
	    13:00
	   </td>
	   <td align='left' style='color: rgb(63, 63, 63);'>
	    Окончание 2 раунда SnarkNews Summer Series - 2011 
	   </td>
	   <td>
	    <a style='color: rgb(67, 105, 172);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>

	  
	   <tr class='table_body'> 
	   <td style='color: rgb(66, 66, 66);'>
	    23.08.2011 
	   </td>
	   <td style='color: rgb(66, 66, 66);'> 
	    14:00
	   </td>
	   <td align='left' style='color: rgb(66, 66, 66);'>
	    Окончание 3 раунда SnarkNews Summer Series - 2011 
	   </td>
	   <td>

	    <a style='color: rgb(70, 107, 171);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>
	  
	   <tr class='CurrentContest'> 
	   <td style='color: rgb(69, 69, 69);'>
	    16.08.2011 
	   </td>
	   <td style='color: rgb(69, 69, 69);'> 
	    07:00
	   </td>

	   <td align='left' style='color: rgb(69, 69, 69);'>
	    2011 Multi-University Training Contest 11 - Host by BJTU. Hangzhou Dianzi University 
	   </td>
	   <td>
	    <a style='color: rgb(73, 109, 171);' href='http://acm.hdu.edu.cn
'>acm.hdu.edu.cn
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(73, 73, 73);'>

	    18.08.2011 
	   </td>
	   <td style='color: rgb(73, 73, 73);'> 
	    07:00
	   </td>
	   <td align='left' style='color: rgb(73, 73, 73);'>
	    Alibaba Programming Open 2011. Hangzhou Dianzi University 
	   </td>
	   <td>
	    <a style='color: rgb(76, 111, 171);' href='http://acm.hdu.edu.cn
'>acm.hdu.edu.cn
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(76, 76, 76);'>
	    19.08.2011 
	   </td>
	   <td style='color: rgb(76, 76, 76);'> 
	    14:00
	   </td>
	   <td align='left' style='color: rgb(76, 76, 76);'>
	    Начало 4 раунда SnarkNews Summer Series - 2011 
	   </td>

	   <td>
	    <a style='color: rgb(79, 113, 171);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(79, 79, 79);'>
	    28.08.2011 
	   </td>
	   <td style='color: rgb(79, 79, 79);'> 
	    14:00
	   </td>

	   <td align='left' style='color: rgb(79, 79, 79);'>
	    Окончание 4 раунда SnarkNews Summer Series - 2011 
	   </td>
	   <td>
	    <a style='color: rgb(83, 115, 171);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(83, 83, 83);'>

	    19.08.2011 
	   </td>
	   <td style='color: rgb(83, 83, 83);'> 
	    18:00
	   </td>
	   <td align='left' style='color: rgb(83, 83, 83);'>
	    Codeforces Beta Round #82 (Div. 2) 
	   </td>
	   <td>
	    <a style='color: rgb(86, 117, 171);' href='http://codeforces.ru
'>codeforces.ru
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(86, 86, 86);'>
	    20.08.2011 
	   </td>
	   <td style='color: rgb(86, 86, 86);'> 
	    19:00
	   </td>
	   <td align='left' style='color: rgb(86, 86, 86);'>
	    TopCoder Single Round Match 515 
	   </td>

	   <td>
	    <a style='color: rgb(89, 119, 171);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(89, 89, 89);'>
	    21.08.2011 
	   </td>
	   <td style='color: rgb(89, 89, 89);'> 
	    09:00
	   </td>

	   <td align='left' style='color: rgb(89, 89, 89);'>
	    Программирование - профессионалы (ком. 2011). Гомельский государственный университет 
	   </td>
	   <td>
	    <a style='color: rgb(92, 121, 171);' href='http://dl.gsu.by
'>dl.gsu.by
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(93, 93, 93);'>

	    23.08.2011 
	   </td>
	   <td style='color: rgb(93, 93, 93);'> 
	    07:00
	   </td>
	   <td align='left' style='color: rgb(93, 93, 93);'>
	    2011 Multi-University Training Contest 15 - Host by BJTU. Hangzhou Dianzi University 
	   </td>
	   <td>
	    <a style='color: rgb(95, 123, 171);' href='http://acm.hdu.edu.cn
'>acm.hdu.edu.cn
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(96, 96, 96);'>
	    23.08.2011 
	   </td>
	   <td style='color: rgb(96, 96, 96);'> 
	    18:00
	   </td>
	   <td align='left' style='color: rgb(96, 96, 96);'>
	    Codeforces Beta Round #83 (Div. 1 Only) 
	   </td>

	   <td>
	    <a style='color: rgb(99, 125, 171);' href='http://codeforces.ru
'>codeforces.ru
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(99, 99, 99);'>
	    23.08.2011 
	   </td>
	   <td style='color: rgb(99, 99, 99);'> 
	    18:00
	   </td>

	   <td align='left' style='color: rgb(99, 99, 99);'>
	    Codeforces Beta Round #83 (Div. 2 Only) 
	   </td>
	   <td>
	    <a style='color: rgb(102, 127, 171);' href='http://codeforces.ru
'>codeforces.ru
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(103, 103, 103);'>

	    25.08.2011 
	   </td>
	   <td style='color: rgb(103, 103, 103);'> 
	    07:00
	   </td>
	   <td align='left' style='color: rgb(103, 103, 103);'>
	    2011 Multi-University Training Contest 16 - Host by BJTU. Hangzhou Dianzi University 
	   </td>
	   <td>
	    <a style='color: rgb(105, 129, 171);' href='http://acm.hdu.edu.cn
'>acm.hdu.edu.cn
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(106, 106, 106);'>
	    26.08.2011 
	   </td>
	   <td style='color: rgb(106, 106, 106);'> 
	    14:00
	   </td>
	   <td align='left' style='color: rgb(106, 106, 106);'>
	    Начало 5 раунда SnarkNews Summer Series - 2011 
	   </td>

	   <td>
	    <a style='color: rgb(108, 131, 171);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(109, 109, 109);'>
	    02.09.2011 
	   </td>
	   <td style='color: rgb(109, 109, 109);'> 
	    17:00
	   </td>

	   <td align='left' style='color: rgb(109, 109, 109);'>
	    Окончание 5 раунда SnarkNews Summer Series - 2011 
	   </td>
	   <td>
	    <a style='color: rgb(112, 133, 171);' href='http://contests.snarknews.info
'>contests.snarknews.info
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(113, 113, 113);'>

	    28.08.2011 
	   </td>
	   <td style='color: rgb(113, 113, 113);'> 
	    07:00
	   </td>
	   <td align='left' style='color: rgb(113, 113, 113);'>
	    ZOJ Monthly, August 2011. Zhejiang University 
	   </td>
	   <td>
	    <a style='color: rgb(115, 135, 171);' href='http://acm.zju.edu.cn
'>acm.zju.edu.cn
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(116, 116, 116);'>
	    30.08.2011 
	   </td>
	   <td style='color: rgb(116, 116, 116);'> 
	    18:00
	   </td>
	   <td align='left' style='color: rgb(116, 116, 116);'>
	    TopCoder Single Round Match 516 
	   </td>

	   <td>
	    <a style='color: rgb(118, 137, 171);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(119, 119, 119);'>
	    04.09.2011 
	   </td>
	   <td style='color: rgb(119, 119, 119);'> 
	    09:00
	   </td>

	   <td align='left' style='color: rgb(119, 119, 119);'>
	    Программирование - профессионалы (ком. 2011). Гомельский государственный университет 
	   </td>
	   <td>
	    <a style='color: rgb(121, 139, 170);' href='http://dl.gsu.by
'>dl.gsu.by
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(123, 123, 123);'>

	    10.09.2011 
	   </td>
	   <td style='color: rgb(123, 123, 123);'> 
	    19:00
	   </td>
	   <td align='left' style='color: rgb(123, 123, 123);'>
	    TopCoder Single Round Match 517 
	   </td>
	   <td>
	    <a style='color: rgb(124, 141, 170);' href='http://topcoder.com
'>topcoder.com
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(126, 126, 126);'>
	    11.09.2011 
	   </td>
	   <td style='color: rgb(126, 126, 126);'> 
	    09:00
	   </td>
	   <td align='left' style='color: rgb(126, 126, 126);'>
	    Программирование - профессионалы (ком. 2011). Гомельский государственный университет 
	   </td>

	   <td>
	    <a style='color: rgb(128, 143, 170);' href='http://dl.gsu.by
'>dl.gsu.by
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(129, 129, 129);'>
	    14.09.2011 
	   </td>
	   <td style='color: rgb(129, 129, 129);'> 
	    14:00
	   </td>

	   <td align='left' style='color: rgb(129, 129, 129);'>
	    TopCoder Single Round Match 518 
	   </td>
	   <td>
	    <a style='color: rgb(131, 145, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(133, 133, 133);'>

	    18.09.2011 
	   </td>
	   <td style='color: rgb(133, 133, 133);'> 
	    09:00
	   </td>
	   <td align='left' style='color: rgb(133, 133, 133);'>
	    Программирование - профессионалы (ком. 2011). Гомельский государственный университет 
	   </td>
	   <td>
	    <a style='color: rgb(134, 147, 170);' href='http://dl.gsu.by
'>dl.gsu.by
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(136, 136, 136);'>
	    20.09.2011 
	   </td>
	   <td style='color: rgb(136, 136, 136);'> 
	    04:00
	   </td>
	   <td align='left' style='color: rgb(136, 136, 136);'>
	    TopCoder Single Round Match 519 
	   </td>

	   <td>
	    <a style='color: rgb(137, 149, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(139, 139, 139);'>
	    04.10.2011 
	   </td>
	   <td style='color: rgb(139, 139, 139);'> 
	    18:00
	   </td>

	   <td align='left' style='color: rgb(139, 139, 139);'>
	    TopCoder Single Round Match 520 
	   </td>
	   <td>
	    <a style='color: rgb(141, 151, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(143, 143, 143);'>

	    13.10.2011 
	   </td>
	   <td style='color: rgb(143, 143, 143);'> 
	    14:00
	   </td>
	   <td align='left' style='color: rgb(143, 143, 143);'>
	    TopCoder Single Round Match 521 
	   </td>
	   <td>
	    <a style='color: rgb(144, 153, 170);' href='http://topcoder.com
'>topcoder.com
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(146, 146, 146);'>
	    26.10.2011 
	   </td>
	   <td style='color: rgb(146, 146, 146);'> 
	    04:00
	   </td>
	   <td align='left' style='color: rgb(146, 146, 146);'>
	    TopCoder Single Round Match 522 
	   </td>

	   <td>
	    <a style='color: rgb(147, 155, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(149, 149, 149);'>
	    12.11.2011 
	   </td>
	   <td style='color: rgb(149, 149, 149);'> 
	    20:00
	   </td>

	   <td align='left' style='color: rgb(149, 149, 149);'>
	    TopCoder Single Round Match 523 
	   </td>
	   <td>
	    <a style='color: rgb(150, 157, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(153, 153, 153);'>

	    17.11.2011 
	   </td>
	   <td style='color: rgb(153, 153, 153);'> 
	    19:00
	   </td>
	   <td align='left' style='color: rgb(153, 153, 153);'>
	    TopCoder Single Round Match 524 
	   </td>
	   <td>
	    <a style='color: rgb(153, 159, 170);' href='http://topcoder.com
'>topcoder.com
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(156, 156, 156);'>
	    29.11.2011 
	   </td>
	   <td style='color: rgb(156, 156, 156);'> 
	    15:00
	   </td>
	   <td align='left' style='color: rgb(156, 156, 156);'>
	    TopCoder Single Round Match 525 
	   </td>

	   <td>
	    <a style='color: rgb(157, 161, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(159, 159, 159);'>
	    07.12.2011 
	   </td>
	   <td style='color: rgb(159, 159, 159);'> 
	    05:00
	   </td>

	   <td align='left' style='color: rgb(159, 159, 159);'>
	    TopCoder Single Round Match 526 
	   </td>
	   <td>
	    <a style='color: rgb(160, 163, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(163, 163, 163);'>

	    17.12.2011 
	   </td>
	   <td style='color: rgb(163, 163, 163);'> 
	    20:00
	   </td>
	   <td align='left' style='color: rgb(163, 163, 163);'>
	    TopCoder Single Round Match 527 
	   </td>
	   <td>
	    <a style='color: rgb(163, 165, 170);' href='http://topcoder.com
'>topcoder.com
</a>

	   </td>
	  </tr>
	  
	   <tr class='table_body'> 
	   <td style='color: rgb(166, 166, 166);'>
	    28.12.2011 
	   </td>
	   <td style='color: rgb(166, 166, 166);'> 
	    19:00
	   </td>
	   <td align='left' style='color: rgb(166, 166, 166);'>
	    TopCoder Single Round Match 528 
	   </td>

	   <td>
	    <a style='color: rgb(166, 167, 170);' href='http://topcoder.com
'>topcoder.com
</a>
	   </td>
	  </tr>
	   </table>
 </div>


 <p><div class='server_info'>Время на сервере: 16.08.2011 18:16:23 &nbsp&nbsp Время последнего обновления: 09.08.2011 14:51:35 </div><div class='server_info'>Мозырь. Клуб юных пожарных (КЮП)</div>

</body>
</html>



            """

        else :
            webpage = urlfetch.fetch( "http://fs13.net/events/" ) 
            f = webpage.content 
        
        pattern = ur"""
            \s+<tr\ class=\'[A-Za-z_]+\'>\s+
            \s+<td\ style=\'color:\ rgb.*\s+
            \s+(\d+.\d+.\d+)\s+                 # date
            \s+</td>\s+
            \s+<td\ style=\'color:\ rgb.*\s+
            \s+(\d+:\d+)\s?                     # time
            \s+</td>\s+
            \s+
            \s+<td\ align=.*>\s?
            \s+(.*)                             # name
            \s+</td>\s?
            \s+<td>\s?
            \s+<a\ .*
            \s+\'>(.*)\s?                       # url
            """

        reg = re.compile( pattern, re.VERBOSE | re.UNICODE )
        matches = reg.finditer( f )       
        
        # pushing the contests into datastore
        for match in matches:
            date = self.get_date( match.group(1), match.group(2) )
            detailed_date = self.get_detail( date )
            time = self.get_time( date )
            name = match.group( 3 )
            location = match.group( 4 )

            if location in russia:
                continue
            else :
                contest = Contest( 
                    date = date, 
                    detailed_date = detailed_date, 
                    time = time,
                    name = name,
                    location = location
                )
                contest.put()
    

    @get_user
    def get(self):
        
        self.load_contests()

        q = db.Query( Contest )
        q.order( "date" )
        contests = q.fetch(10) 
    
        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'contests'  : contests 
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'contests.html' )
        self.response.out.write( template.render( path, template_values ) )



