import web
import os
import sys
import re
import glob


urls = (
    '/', 'index',
    '/post', 'post',
    '/doxviewer', 'archive',
    '/doxviewer/(.*)', 'doxviewer',
    '/proscription', 'proscription',
    '/privacy', 'privacy',
    '/faq', 'faq',
)

render = web.template.render('templates')

class index:
    def GET(self):
        return render.index()

class post:
    def POST(self):
        basicData = "<!DOCTYPE html><html><head><title>DOXBIN</title></head><body>%s</body></html>"

        if os.path.exists('dox/DISABLEPOST'):
            return 'Posting is gay.'

        self.input = web.input()

        if self.input:
            try:
                name = re.sub(r'[<>|#${}.()/\\]', '_', self.input['name'].strip().rstrip())
                dox = re.sub(r'[<>|#${}.()/\\]', '_', self.input['dox'])
                if name == "" or dox == "":
                    return basicData%"You didn't put in anything retard."
                fileName = name + ".txt"
                if os.path.exists("dox/%s"%fileName):
                    return basicData%'Already exists idiot.'
                fileWrite = open('dox/%s'%fileName, 'w')
                fileWrite.write(dox)
                fileWrite.close()
                return basicData%'Dox was posted. Read it over <a href="/doxviewer/%s">here.</a> or post more <a href="/">here.</a>'%fileName.split('.txt')[0]
            except ValueError:
                return 'Hecker Scum!'
            except:
                return 'Unhandled exception, contact staff if important.'
        else:
            return 'No input, hecker scum?'

class doxviewer:
    def GET(self, dox):
        if dox == "":
            return render.doxerviewer("Hecker Scum!")
        dox = re.sub(r'[<>|#${}.()/\\]', '_', dox)
        return render.doxviewer(open('dox/%s.txt'%dox, 'r').read())

class archive:
    def GET(self):
        html = ""
        doxs = glob.glob('dox/*.txt')
        for dox in doxs:
            html += '<a href="/doxviewer/%s">%s</a><br/>\n'%(dox.split('\\')[1].split('.txt')[0], dox.split('\\')[1].split('.txt')[0])
        return render.archive(html)

class proscription:
    def GET(self):
        return render.proscription()

class privacy:
    def GET(self):
        return render.privacy()

class faq:
    def GET(self):
        return render.faq()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()