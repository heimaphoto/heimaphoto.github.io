package main
import (
        "os"
        "fmt"
        "strings"
        "strconv"
)

var i int64

func main() {
    index()

}

func index() {
    lujing := "./post/"
    dir, _ := os.Open(lujing)
    files, _ := dir.Readdir(0)
    name := make(map[int64]string)
    i = 0
    for _, a := range files {
        if !a.IsDir() {
            b := a.Name()
            c := strings.Split(b,"-")
            e := strings.Split(c[1],".")
            d, err := strconv.ParseInt(c[0],10,64)
            if err != nil {
                panic(err)
            }
            name[d] = e[0]
            if i < d {
                i = d
            }

        }
    }
    fmt.Printf("%s\n",name[i])
    ff, err := os.Open("./mo/index.mo")
    defer ff.Close()
    if err != nil {
        panic(err)
    }
    mode := ""
    buf := make([]byte,1024)
    for {
        n, _ := ff.Read(buf)
        if n == 0 { break }
        mode = mode + string(buf[:n])
    }
    ci := i
    mode = strings.Replace(mode,"\r","",-1)
    recent := ""
    htmlstart := "<tr><td width=\"100\"></td>\n<td width=\"200\"><div class=\"indextext\"><a href=\"./post/"
    html2 := "</a></div></td>\n<td><div class=\"indextitle\"><a href=\"./post/"
    for ii := 1; ii < 11; ii++ {
        if ci > 0 {
            readfile := strconv.FormatInt(ci,10) + "-" + name[ci] + ".htm"
            ff2, err := os.Open("./post/" + readfile)
            if err != nil { panic(err) }
            buf2 := make([]byte,1024)
            rtext := ""
            for {
                n, _ := ff2.Read(buf2)
                if n == 0 { break }
                rtext = rtext + string(buf2[:n])
            }
            t2 := strings.Split(rtext,"<title>")
            t3 := strings.Split(t2[1],"</title>")
            title := t3[0]
            ti2 := strings.Split(rtext,">Written on ")
            ti3 := strings.Split(ti2[1]," | Tag:")
            time := ti3[0]
            tagname := "未定义"
            if name[ci] == "prose" { tagname = "散文" }
            if name[ci] == "TheArtOfSeeing" { tagname = "看的艺术" }
            recent = recent + htmlstart + readfile + "\">" + time + "--" + tagname + html2 + readfile + "\">" + title + "</a></div></td>\n</tr>\n"
            ci = ci - 1
        }
    }
    indextext := strings.Replace(mode,"[RECENT]",recent,1)
    ff3,err := os.Create("index.html")
    defer ff3.Close()
    if err != nil { panic(err) }
    ff3.WriteString(indextext)
}
