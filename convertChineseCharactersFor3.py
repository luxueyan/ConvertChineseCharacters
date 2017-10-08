#-*- coding: utf-8 -*-
import sublime
import sublime_plugin
import sys
import re
jsExt = ["js", "json"]
cssExt = ["css", "less", "sass"]
htmlExt = ["html", "vue", "jade", "pug"]


class ChineseCharactersToUnicodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        fileName = self.view.file_name()
        fileSuffix = re.match(r'.+\.(\w+)$', fileName).group(1)
        # if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css":

        def TU(x):
            if fileSuffix in jsExt:
                return '\\u' + ('000' + hex(ord(x))[2:])[-4:]
            elif fileSuffix in htmlExt:
                return '&#x' + ('000' + hex(ord(x))[2:])[-4:] + ';'
            elif fileSuffix in cssExt:
                return '\\' + ('000' + hex(ord(x))[2:])[-4:]

        def toUnicode(x):
            s = x.group(0)
            s = list(s)
            mapValue = map(TU, s)
            s = "".join(mapValue)
            return s

        def convertToUnicode(region):
            s = self.view.substr(region)
            s = re.sub(r"([\u4e00-\u9fa5]+)", toUnicode, s)
            self.view.replace(edit, region, s)

        regions = self.view.sel()
        if not regions[0].empty():
            for region in regions:
                if not region.empty():
                   convertToUnicode(region) 
        else:
            region = sublime.Region(0, self.view.size())
            convertToUnicode(region)
        # else:
        #     sublime.error_message('不能解析的文件类型')


class UnicodeToChineseCharactersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fileName = self.view.file_name()
        fileSuffix = re.match(r'.+\.(\w+)$', fileName).group(1)
        # if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css" or fileSuffix == "vue" or fileSuffix == "pug":

        def unicodeTo(x):
            s = x.group(0)
            if fileSuffix in jsExt:
                s = s[2:]
            elif fileSuffix in htmlExt:
                s = s[3:-1]
            elif fileSuffix in cssExt:
                s = s[1:]
            s = chr(int(s, 16))
            return s

        def convertToChinese(region):
            s = self.view.substr(region)
            if fileSuffix in jsExt:
                s = re.sub(r"(\\[uU]\w{4})", unicodeTo, s)
            elif fileSuffix in htmlExt:
                s = re.sub(r"(&#x\w{4};)", unicodeTo, s)
            elif fileSuffix in cssExt:
                s = re.sub(r"(\\\w{4})", unicodeTo, s)
            self.view.replace(edit, region, s)

        regions = self.view.sel()
        if not regions[0].empty():
            for region in regions:
                if not region.empty():
                    convertToChinese(region)
        else:
            region = sublime.Region(0, self.view.size())
            convertToChinese(region)
        # else:
        #     sublime.error_message('不能解析的文件类型')
