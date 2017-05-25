package main
import (
        "os"
        "fmt"
        "strings"
        "strconv"
        "regexp"
        "io/ioutil"
)

var i int64=0
var lujing string=""
var newname string
var lastname string
var modeFile string=""
var IMGNAME string=""
var MoBan string=""
var Title string=""
var Content string=""
var mode string=""
var IMG1 string=""
var wri string=""
var post string=""
var meta string=""
var message string=""
var Time string=""
var tag string=""
var tagurl string=""
var tagurlpre string=""
var nav string=""

func main() {
    readtext()
    creattagurl()
    newfilename()
    fmt.Printf("%s\n",newname)
    readmode()
    texttohtml()
    writefile()
}

func newfilename() {
       lujing = "./post/"
       dir, _ := os.Open(lujing)
       files, _ := dir.Readdir(0)
       var b string
       var c []string
       for _, a := range files {
           if !a.IsDir() {
               b = a.Name()
               c = strings.Split(b,"-")
               d, err := strconv.ParseInt(c[0],10,64)
               if err != nil {
                   panic(err)
               }
               if i<d {
                   i = d
                   tagurlpre = strings.Split(c[1],".")[0]
               }
           }
       }
       newname = strconv.FormatInt(i+1,10) + "-" + tagurl + ".htm"
       lastname = strconv.FormatInt(i,10) + "-" + tagurlpre + ".htm"
}

func readmode() {
    buf, err := ioutil.ReadFile(modeFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    mode = string(buf)
}

func readtext() {
    inputFile := "post.md"
    buf, err := ioutil.ReadFile(inputFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    alltext := string(buf)
    reg1 := regexp.MustCompile(`\[Title\]\n(.+)\n\[/Title\]`)
    s1 := reg1.FindString(alltext)
    s2 := "$1"
    Title = reg1.ReplaceAllString(s1,s2)
    fmt.Printf("标题是：%s\n",Title)
    reg2 := regexp.MustCompile(`\[MoBan\]\n(.+)\n\[/MoBan\]`)
    s3 := reg2.FindString(alltext)
    s4 := "$1"
    MoBan = reg2.ReplaceAllString(s3,s4)
    fmt.Printf("使用模板：%s\n",MoBan)
    reg3 := regexp.MustCompile(`\[Time\]\n(.+)\n\[/Time\]`)
    s5 := reg3.FindString(alltext)
    s6 := "$1"
    Time = reg3.ReplaceAllString(s5,s6)
    fmt.Printf("发表日期：%s\n",Time)
    reg4 := regexp.MustCompile(`\[TAG\]\n(.+)\n\[/TAG\]`)
    s7 := reg4.FindString(alltext)
    s8 := "$1"
    tag = reg4.ReplaceAllString(s7,s8)
    fmt.Printf("TAG：%s\n",tag)
    reg5 := regexp.MustCompile(`\[Content\]\n([\s\S]+)\n\[/Content\]`)
    s9 := reg5.FindString(alltext)
    s10 := "$1"
    Content = reg5.ReplaceAllString(s9,s10)
    fmt.Printf("文章内容：%s\n",Content)
    reg6 := regexp.MustCompile(`\[IMGNAME\]\n([\s\S]+)\n\[/IMGNAME\]`)
    s11 := reg6.FindString(alltext)
    s12 := "$1"
    IMGNAME = reg6.ReplaceAllString(s11,s12)
    fmt.Printf("照片名称：%s\n",IMGNAME)
    if MoBan == "1" {
        modeFile = "./mo/article1.mo"
    }
    if MoBan == "2" {
        modeFile = "./mo/article2.mo"
    }
    if MoBan == "3" {
        modeFile = "./mo/article3.mo"
    }
}

func creattagurl() {
    if tag == "散文" {
        tagurl = "prose"
    }
    if tag == "七种武器" {
        tagurl = "equipment"
    }
    if tag == "摄影技术" {
        tagurl = "photography"
    }
    if tag == "看的艺术" {
        tagurl = "TheArtOfSeeing"
    }
    if tag == "论坛" {
        tagurl = "discuss"
    }

}

func texttohtml() {
    meta = "<div class=\"meta\">Written on " + Time + " | Tag: <a href=\"../archive/" + tagurl + "1.htm\">" + tag + "</a></div>"
    message = "<div class=\"mess\"><a href=\"http://www.douban.com/group/heimaphoto/\" target=\"_blank\">留言或讨论请点击这里</a></div>"
    IMGNAME = strings.Replace(IMGNAME," ","",0)
    if MoBan == "1" || MoBan == "2" {
        post = ""
        if strings.Contains(IMGNAME,"\n") {
            IMG1 = strings.Split(IMGNAME,"\n")[0]
        } else {
            IMG1 = IMGNAME
        }
    } else {
        IMG2 := strings.Split(IMGNAME,"\n")
        IMG1 = IMG2[0]
        XunHuan := ""
        for u := 1; u < len(IMG2); u++ {
            XunHuan = "<tr><td>\n"
            XunHuan = XunHuan + "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"10\">\n"
            XunHuan = XunHuan + "<tr><td><img src=\"../../images/myphoto/" + IMG2[u] + "\"></td></tr>\n"
            XunHuan = XunHuan + "<tr><td><div class=\"photoinfo\"></div></td></tr></table>\n"
            XunHuan = XunHuan + "</td></tr>\n\n"
            post = post + XunHuan
            XunHuan = ""
        }
    }
    if i == 0 {
        nav = ""
    } else {
        nav = "<a href=\"./" + lastname + "\">上一篇</a>"
    }
}

func writefile() {
    wFile := lujing + newname
    fout,err := os.Create(wFile)
    defer fout.Close()
    if err != nil {
            fmt.Println(wFile,err)
            return
    }
    wri = strings.Replace(mode,"[title]",Title,1)
    wri = strings.Replace(wri,"[img]",IMG1,1)
    wri = strings.Replace(wri,"[Content]",Content,1)
    wri = strings.Replace(wri,"[post]",post,1)
    wri = strings.Replace(wri,"[meta]",meta,1)
    wri = strings.Replace(wri,"[message]",message,1)
    wri = strings.Replace(wri,"[nav]",nav,1)
    fout.WriteString(wri)
    if i != 0 {
        preFile := lujing + lastname
        buf, err := ioutil.ReadFile(preFile)
        if err != nil {
            fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
            // panic(err.Error())
        }
        alltext := string(buf)

        if !strings.Contains(alltext,"下一篇</a>") {
            if i == 1 {
                oldtext := "索引页</a> | "
                replacetext := oldtext + "<a href=\"./" + newname + "\">下一篇</a>"
                alltext = strings.Replace(alltext,oldtext,replacetext,1)
                fin2, err := os.OpenFile(preFile,os.O_RDWR | os.O_TRUNC,0644)
                defer fin2.Close()
                fin2.WriteString(alltext)
                fin2.Close()
            } else {
                oldtext := "上一篇</a>"
                replacetext := oldtext + " | <a href=\"./" + newname + "\">下一篇</a>"
                alltext = strings.Replace(alltext,oldtext,replacetext,1)
                fin2, err := os.OpenFile(preFile,os.O_RDWR | os.O_TRUNC,0644)
                defer fin2.Close()
                fin2.WriteString(alltext)
                fin2.Close()
            }
        }
    }
}
