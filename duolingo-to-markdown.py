
import requests, os, sys


def duolingo_request():
    session = requests.Session()
    username = os.getenv('DUOLINGO_USERNAME')
    password = os.getenv('DUOLINGO_PASSWORD')
    session.send( requests.Request('POST', url = "https://www.duolingo.com/login",
                                   json = {"login": "{}".format(username), "password": "{}".format(password)} ).prepare())
    response = requests.get("https://www.duolingo.com/api/1/users/show?username={}".format(username), cookies=session.cookies)
    
    if response.status_code == 200:
        response = response.json()
        return response
    sys.exit("Incorrect password or username. Please try again with another vaues.")


def get_duloingo_info(response):
    num_language = int(os.getenv('DUOLINGO_LANGUAGE_LENGTH'))
    lang_list = [( language_list["language_string"],language_list["level"], language_list["points"] ) for language_list in response["languages"] if language_list["learning"] == True]
    lang_list.sort(key=lambda lang:lang[2], reverse= True)
    lang_list = [lang for lang in lang_list[:num_language] if lang[2]>0]
    return lang_list
 
 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def update_readme(response):
    username = os.getenv('DUOLINGO_USERNAME')
    streak_str = os.getenv('DUOLINGO_STREAK')
    with open('README.md', 'r', encoding='utf-8') as file:
        readme = file.readlines()
    try:
        duolingo_line_index = readme.index('<!-- duolingo -->\n') + 1
    except:
        sys.exit("Could not find '<!-- duolingo -->' in your README.md")
    duolingo_line = '<p align="center">'
    
    duolingo_line += '<img src="https://d35aaqx5ub95lt.cloudfront.net/images/dc30aa15cf53a51f7b82e6f3b7e63c68.svg">  Duolingo username: <strong> {} </strong> </br>'.format(username)
    if streak_str == 'true':
        duolingo_line += 'Last Streak: <strong> {}</strong>  <img   width="20.5px" height="15.5px" src="https://d35aaqx5ub95lt.cloudfront.net/vendor/398e4298a3b39ce566050e5c041949ef.svg"></br>'.format(response["last_streak"]["length"])   
    
    lang_list = get_duloingo_info(response)
    
    duolingo_line += """<table align="center"><tr><th>Language</th><th>Level</th><th>Experience</th></tr>""" 
    for lang in lang_list:
        duolingo_line += """ <tr><th>{} </th><th><span><img  width="20.5px" height="15.5px"  src="https://d35aaqx5ub95lt.cloudfront.net/vendor/b3ede3d53c932ee30d981064671c8032.svg"><span >{}</span></span></th><th><span><img width="20.5px" height="15.5px" src="https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"><span >{}</span></span></th></tr>""".format(lang[0], lang[1], lang[2])
    if (readme[duolingo_line_index] == duolingo_line):
        sys.exit(0)
    else:
        duolingo_line = duolingo_line + '</table></p> \n'
        readme[duolingo_line_index] = duolingo_line
    with open('README.md', 'w', encoding='utf-8') as file:
        file.writelines(readme)



update_readme(duolingo_request())
