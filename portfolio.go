package main

import (
    "os"
    "fmt"
    "strings"
    "strconv"
    "regexp"
    "io/ioutil"
)

var lujing string=""
var i int64=0
var u int64=0
var newname string=""
var lastname string=""
var post string=""
var Title string=""
var TitleCN string=""
var TitleEN string=""
var PhotoName string=""
var PhotoInfo string=""

func main() {
     newfilename()
     readtext()
     writehtm()
     editlastname()
     readportfolio()
}

func newfilename() {
    lujing = "./doc/"
    dir, _ := os.Open(lujing)
    files, _ := dir.Readdir(0)
    var b string
    var c string
    for _, a := range files {
    if !a.IsDir() {
        b = a.Name()
        c = strings.Replace(strings.Split(b,".")[0],"wangbin","",-1)
        d, err := strconv.ParseInt(c,10,64)
        if err != nil {
            panic(err)
        }
        if i<d {
            i = d
        }
    }
  }
  newname = "wangbin" + strconv.FormatInt(i+1,10) + ".htm"
  lastname = "wangbin" + strconv.FormatInt(i,10) + ".htm"
}

func readtext() {
    inputFile := "portfolio.po"
    buf, err := ioutil.ReadFile(inputFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    fmt.Printf("%s\n", string(buf))
    post = string(buf)
    reg1 := regexp.MustCompile(`\[Title\]\n([\s\S]+)\n\[/Title\]`) // 这里要读取[Title]...[/Title]标签中间的内容
    s1 := reg1.FindString(post)
    s2 := "$1"
    s3 := strings.Split(reg1.ReplaceAllString(s1,s2),"\n")
    TitleCN = s3[0]
    TitleEN = s3[1]
    Title = "黑马摄影-" + TitleCN + "-" + TitleEN
    fmt.Printf("标题是：%s\n",Title)
    reg2 := regexp.MustCompile(`\[PhotoName]\n(.+)\n\[/PhotoName\]`)
    s4 := reg2.FindString(post)
    s5 := "$1"
    PhotoName = reg2.ReplaceAllString(s4,s5)
    reg3 := regexp.MustCompile(`\[PhotoInfo]\n([\s\S]+)\n\[/PhotoInfo\]`)
    s6 := reg3.FindString(post)
    s7 := "$1"
    PhotoInfo = reg3.ReplaceAllString(s6,s7)
    PhotoInfo = strings.Replace(PhotoInfo," ","",-1)
    PhotoInfo = strings.Replace(PhotoInfo,"\n","<br />",-1)
}

func writehtm() {
    alltext := ""
    inputFile := "./Templates/htm.mo"
    buf, err := ioutil.ReadFile(inputFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
    }
    alltext = string(buf)
    wri := ""
    wri = strings.Replace(alltext,"[Title]",Title,1)
    wri = strings.Replace(wri,"[Title-CN]",TitleCN,1)
    wri = strings.Replace(wri,"[Title-EN]",TitleEN,1)
    wri = strings.Replace(wri,"[PhotoInfo]",PhotoInfo,1)
    wri = strings.Replace(wri,"[PhotoName]",PhotoName,1)
    wri = strings.Replace(wri,"[lastname]",lastname,1)

    wFile := "./doc/" + newname
    fout,err := os.Create(wFile)
    defer fout.Close()
    if err != nil {
        fmt.Println(wFile,err)
        return
    }
    fout.WriteString(wri)
}

func editlastname() {
    inputFile := lujing + lastname
    buf, err := ioutil.ReadFile(inputFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
    }
    alltext := ""
    alltext = string(buf)
    oldtext := "<a href=\"#\">下一张</a>"
    newtext := "<a href=\"" + newname + "\">" + "下一张</a>"
    alltext = strings.Replace(alltext,oldtext,newtext,1)
    fin2, err := os.OpenFile(inputFile,os.O_RDWR | os.O_TRUNC,0644)
    defer fin2.Close()
    fin2.WriteString(alltext)
    fin2.Close()
}

func readportfolio() {
    dir, _ := os.Open("./")
    files, _ := dir.Readdir(0)
    var b string=""
    var c string=""
    for _, a := range files {
        if !a.IsDir() {
            b = a.Name()
            if strings.Contains(b,"portfolio") {
                c = strings.Replace(strings.Split(b,".")[0],"portfolio","",-1)
            }
            if c != "" {
                d, err := strconv.ParseInt(c,10,64)
                if err != nil {
                    panic(err)
                }
                if u<d {
                    u = d
                }
            }
        }
    }
    portfolioName := "portfolio" + strconv.FormatInt(u,10) + ".htm"
    ii := i + 1
    if ii % 20 == 1 {
        u = u + 1
        portfolioName = "portfolio" + strconv.FormatInt(u,10) + ".htm"
        lastportfolioName := "portfolio" + strconv.FormatInt(u-1,10) + ".htm"
        alltext := ""
        inputFile := "./Templates/portfolio.mo"
        buf, err2 := ioutil.ReadFile(inputFile)
        if err2 != nil {
            fmt.Fprintf(os.Stderr, "File Error: %s\n", err2)
            // panic(err.Error())
        }
        alltext = string(buf)
        Nav := ""
        var uuu int64=0
        for uuu = 1; uuu < u+1; uuu++ {
            if u == 1 {
            Nav = " | <font color=\"#006699\">" + strconv.FormatInt(u,10) + "</font>"
            break
            }
            if uuu == 1 {
            Nav = "<a href=\"./" + lastportfolioName + "\">上一页</a> | <font color=\"#006699\">Page</font>"
            Nav = Nav + " | <a href=\"portfolio.htm\">" + strconv.FormatInt(uuu,10) + "</a>"
            } else {
                if uuu == u {
                Nav = Nav + " | <font color=\"#006699\">" + strconv.FormatInt(u,10) + "</font>"
                } else {
                Nav = Nav + " | <a href=\"" + "portfolio" + strconv.FormatInt(uuu,10) + ".htm" + "\">" + strconv.FormatInt(uuu,10) + "</a>"
                }
            }
        }
        wri := ""
        oldtext := "<div class=\"empty\"></div>"
        newtext := "<a href=\"./doc/" +newname + "\"><img src=\"./img/logo/" + "wangbin0" + strconv.FormatInt(i+1,10) + "-logo.jpg\" width=\"150\" height=\"100\" alt=\"" + TitleCN + "\"></a>"
        wri = strings.Replace(alltext,"[Nav]",Nav,1)
        wri = strings.Replace(alltext,oldtext,newtext,1)
        fout,err3 := os.Create(portfolioName)
        defer fout.Close()
        if err3 != nil {
            fmt.Println(portfolioName,err3)
            return
        }
        fout.WriteString(wri)
        portfolioNextName := ""
        portfolioIndexName := ""
        docnav := ""
        alltext2 := ""
        oldnav := ""
        newnav := ""
        var oo int64=0
        for oo = 1; oo < u; oo++ {
            portfolioNextName = "portfolio" + strconv.FormatInt(oo+1,10) + ".htm"
            if oo == 1 {
                portfolioIndexName = "portfolio.htm"
            } else {
                portfolioIndexName = "portfolio" + strconv.FormatInt(oo,10) + ".htm"
            }
            if oo == u-1 {
                oldnav = "<a href=\"#\">下一页</a>"
            } else {
                oldnav = "<a href=\"" + portfolioNextName + "\">下一页</a>"
            }
            newnav = "<a href=\"" + portfolioName + "\">" + strconv.FormatInt(u,10) + "</a> | <a href=\"" + portfolioNextName + "\">下一页</a>"
            buf2, err4 := ioutil.ReadFile(portfolioIndexName)
            if err4 != nil {
                fmt.Fprintf(os.Stderr, "File Error: %s\n", err4)
                // panic(err.Error())
            }
            alltext2 = string(buf2)
            docnav = strings.Replace(alltext2,oldnav,newnav,1)
            fin3, _ := os.OpenFile(portfolioIndexName,os.O_RDWR | os.O_TRUNC,0644)
            defer fin3.Close()
            fin3.WriteString(docnav)
            fin3.Close()
        }
    } else {
        wri := ""
        buf, err := ioutil.ReadFile(portfolioName)
        if err != nil {
            fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
            // panic(err.Error())
        }
        alltext :=string(buf)
        oldtext := "<div class=\"empty\"></div>"
        newtext := "<a href=\"./doc/" +newname + "\"><img src=\"./img/logo/" + "wangbin0" + strconv.FormatInt(i+1,10) + "-logo.jpg\" width=\"150\" height=\"100\" alt=\"" + TitleCN + "\"></a>"
        wri = strings.Replace(alltext,oldtext,newtext,1)
        fin2, _ := os.OpenFile(portfolioName,os.O_RDWR | os.O_TRUNC,0644)
        defer fin2.Close()
        fin2.WriteString(wri)
        fin2.Close()
    }
}
