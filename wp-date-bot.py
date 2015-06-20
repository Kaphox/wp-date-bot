import praw
import HTMLParser
import urllib2
import time
 
REDDIT_USERNAME = ''
REDDIT_PASS = ''
SUBREDDIT_NAME = ''
 
def determineMonthByWeekday(d):
    current_day = time.strftime("%A", time.gmtime())
 
    if current_day == "Tuesday":
        month_string = "January/February"
    elif current_day == "Wednesday":
        month_string = "March/April"
    elif current_day == "Thursday":
        month_string = "May/June"
    elif current_day == "Friday":
        month_string = "July/August"
    elif current_day == "Saturday":
        month_string = "September/October"
    elif current_day == "Sunday":
        month_string = "November/December"
    else:
        month_string = "DISCUSSION DAY"
 
    print "Updating month..."
    d['current_months'] = "**" + month_string
 
def determineIfYearNeedsToChange(d):
    year = int(d['current_year'][:-4])
    # Checks if it is after midnight on a Tuesday
    if time.strftime("%A") == 'Tuesday':
        print "Updating year..."
        year += 1
 
    d['current_year'] = str(year) + '**\n\n'
 
def parseSidebar(r, sub):
    while True:
        try:
            settings = r.get_settings(sub)
            break
        except urllib2.HTTPError, e:
            if e.code in [429, 500, 502, 503, 504]:
                print "Reddit is down (Error: {}), sleeping...".format(e.code)
                time.sleep(60)
                pass
            else:
                raise
        except Exception, e:
            print "couldn't Reddit: {}".format(str(e))
            raise
 
    sidebar = settings['description']
    substring = "["
    index = sidebar.find(substring)
 
    print "Parsing Sidebar..."
    current_time_string = sidebar[:index]
    current_time_list = current_time_string.split(' ')
 
    return {'index': index,
            'sidebar': sidebar,
            'current_months': current_time_list[1],
            'current_year': current_time_list[2] }
 
def updateSidebar(r, sub, d):
    new_time_list = ['#####',d['current_months'], d['current_year']]
    new_time_string = (' ').join(new_time_list)
    bottom_of_sidebar = d['sidebar'][d['index']:]
    new_sidebar = HTMLParser.HTMLParser().unescape(new_time_string + bottom_of_sidebar)
 
    print "Updating Sidebar..."
    while True:
        try:
            r.update_settings(sub, description = new_sidebar)
            break
        except urllib2.HTTPError, e:
            if e.code in [429, 500, 502, 503, 504]:
                print "Reddit is down (Error: {}), sleeping...".format(e.code)
                time.sleep(60)
                pass
            else:
                raise
        except Exception, e:
            print "couldn't Reddit: {}".format(str(e))
            raise
 
def main():
    while True:
        try:
            r = praw.Reddit(user_agent = '/r/WorldPowers Sidebar Updater v0.1')
            r.login(REDDIT_USERNAME, REDDIT_PASS)
            sub = r.get_subreddit(SUBREDDIT_NAME)
            break
        except urllib2.HTTPError, e:
            if e.code in [429, 500, 502, 503, 504]:
                print "Reddit is down (Error: {}), sleeping...".format(e.code)
                time.sleep(20)
                pass
            else:
                raise
        except Exception, e:
            print "couldn't Reddit: {}".format(str(e))
            raise
 
    while True:
        if time.strftime("%H %m", time.gmtime()) == "00 00":
            d = parseSidebar(r, sub)
            determineMonthByWeekday(d)
            determineIfYearNeedsToChange(d)
            updateSidebar(r, sub, d)
            return
 
if __name__ == "__main__":
    main()
