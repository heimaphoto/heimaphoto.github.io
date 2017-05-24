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
var mode string=""
var modeFile string=""
var text string
var IMGNAME string
var Title string=""
var Content string=""
var wri string=""
var post string
var Time string=""
var tag string=""
var tagurl string=""
var tagurlpre string=""
var nav string=""
var body string=""

func main() {
    readtext()
    creattagurl()
    newfilename()
    fmt.Printf("%s\n",newname)
    readmode()
    bodytext()
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
    fin,err := os.Open(modeFile)
    defer fin.Close()
    if err != nil {
             fmt.Println(modeFile,err)
             return
     }
     buf := make([]byte, 1024)
     for{
            n, _ := fin.Read(buf)
            if 0 == n { break }
            list := string(buf[:n])
            mode = mode + list
     }

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
    MoBan := reg2.ReplaceAllString(s3,s4)
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

            sp := strings.Split(alltext,"\n\n")
            sp2 := strings.Split(sp[0],"\n")
            if strings.Contains(sp2[0],"[img-H]") {
                img = strings.Replace(sp2[0],"[img-H]","",-1)
                modeFile = "./mo/article.mo"
            }
            if strings.Contains(sp2[0],"[img-S]") {
                img = strings.Replace(sp2[0],"[img-S]","",-1)
                modeFile = "./mo/article2.mo"
            }
            time = sp2[1]
            tag = sp2[2]
            temp := sp[0]+"\n\n"+sp[1]+"\n\n"
            text = strings.Replace(alltext,temp,"",1)
            title = strings.Replace(sp[1],"## ","",1)
            fmt.Printf("tag: %s\n",tag)
            fmt.Printf("img's URL is: %s\n",img)

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
    meta := "</div><div class=\"meta\">Written on " + time + " | Tag: <a href=\"../archive/" + tagurl + "1.htm\">" + tag + "</a>"
    message := "</div><div class=\"mess\"><a href=\"http://www.douban.com/group/heimaphoto/\" target=\"_blank\">留言或讨论请点击这里</a>"
    post = "<h2>" + title + "</h2>" + body + meta + message
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
    wri = strings.Replace(mode,"[title]",title,1)
    wri = strings.Replace(wri,"[img]",img,1)
    wri = strings.Replace(wri,"[post]",post,1)
    wri = strings.Replace(wri,"[nav]",nav,1)
    fout.WriteString(wri)
    if i != 0 {
        preFile := lujing + lastname
        prefout, er := os.Open(preFile)
        defer prefout.Close()
        if er != nil {
            fmt.Println(preFile,er)
            return
        }
        buf := make([]byte, 1024)
        alltext := ""
        for{
            n, _ := prefout.Read(buf)
            if 0 == n { break }
            alltext = alltext + string(buf[:n])
        }
        if !strings.Contains(alltext,"下一篇</a>") {
        if i == 1 {
            oldtext := "索引页</a> | "
            replacetext := oldtext + "<a href=\"./" + newname + "\">下一篇</a>"
            alltext = strings.Replace(alltext,oldtext,replacetext,1)
            prewr, eerr := os.Create(preFile)
            defer prewr.Close()
            if eerr != nil {
                fmt.Println(preFile,eerr)
                return
            }
            prewr.WriteString(alltext)
        } else {
            oldtext := "上一篇</a>"
            replacetext := oldtext + " | <a href=\"./" + newname + "\">下一篇</a>"
            alltext = strings.Replace(alltext,oldtext,replacetext,1)
            prewr, eerr := os.Create(preFile)
            defer prewr.Close()
            if eerr != nil {
                fmt.Println(preFile,eerr)
                return
            }
            prewr.WriteString(alltext)
        }
        }
    }
}

func bodytext() {
    body = "<p>"+strings.Replace(text,"\n\n","</p>\n<p>",-1)+"</p>\n"
    body = strings.Replace(body," \n","<br />\n",-1)
    reg := regexp.MustCompile(`\+ +|- +`)
    list := reg.FindAllString(body,-1)
    st2 := ""
    if len(list) > 0 {
        bodylist := strings.Split(body,"</p>")
        reg2 := regexp.MustCompile(`<p>\+ +|<p>- +`)
        st := ""
        st3 := ""
        for k, v := range bodylist {
           switch k {
                case len(bodylist)-1:
                default:
                if len(reg2.FindAllString(v,-1)) > 0 {
                    if strings.Contains(v,"\r\n") {
                        reg3 := regexp.MustCompile(`\n\+ +|\n- +`)
                        st3 = strings.Replace(v,reg3.FindAllString(v,-1)[0],"</li><li>",-1)
                        st = strings.Replace(st3,reg2.FindAllString(v,-1)[0],"<p><li>",1)
                        st2 = st2 + st + "</li></p>"
                    } else {
                    st = strings.Replace(v,reg2.FindAllString(v,-1)[0],"<p><li>",1)
                    st2 = st2 + st + "</li></p>"
                    }
                } else {
                    st2 = st2 + v + "</p>"
                }
            }
        }
        body = st2
    }
}
