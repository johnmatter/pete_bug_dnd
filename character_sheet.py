from coldtype import *
from coldtype.img.skiaimage import SkiaImage
from coldtype.fx.skia import *
from coldtype.fx.motion import *
from coldtype_pypalettes import *

import json
from lorem.text import TextLorem
import glob
aspect = 16/9
width = 1920
height = width / aspect

# pm = PaletteManager().load_by_index(15)
# pm = PaletteManager().load_by_index(19)
pm = (PaletteManager().load_by_index(54).shuffle(0).rotate(0))
pm = (PaletteManager().load_by_index(
    66)
    .shuffle(
    0)
    .rotate(
    3)
)
# glob in fonts/vf/{style} to get all the variable fonts
deco_fonts = { i: f for i, f in enumerate(glob.glob("fonts/vf/deco/*.ttf")) }
sans_fonts = { i: f for i, f in enumerate(glob.glob("fonts/vf/sans/*.ttf")) }

# load json file
character_json = "stats/bug.json"
# character_json = "stats/pete.json"
character = json.load(open(character_json))
print(character)

papers = { i: f for i, f in enumerate(glob.glob("media/paper/*")) }
paper_filename = papers[6]
paper_filename = "/Users/matter/Downloads/gradient-color-grainy-textures-2023-11-27-05-33-48-utc/gradients/20.jpg" 

stat_frame_filename = "media/frame/a.png"
portrait_frame_filename = "media/frame/c.png"

containers = "/Users/matter/fonts/ohno bangers/Irregardless-Containers.otf"

@animation((width,height), timeline=1)
def scratch(f:Frame):
    composition = P()
    # composition += P().rect(f.a.r).f(pm[0])

    paper = (SkiaImage(paper_filename)
      .align(f.a.r, "SE")
      .scale(1/100)
      .translate(-568, 165)
    )
    composition.insert(0, paper)
    composition.blendmode(BlendMode.Cycle(24))

    # main scaffold
    s_main = Scaffold(f.a.r.inset(0.05*f.a.r.w)).cssgrid("35% a 35%", "a", "a b c")
    # composition += s_main.view()


    #-------------------------------------------------------------------------
    # stat block
    stat_block_guide = P().rect(s_main["a"].r.take(0.73*s_main["a"].r.w, "mdx").take(0.84, "mdy")).f(pm[6])
    composition += stat_block_guide
    stat_block_frame = (SkiaImage(stat_frame_filename)
      .ch(potrace(f.a.r.inset(-1000)))
      .scale(0.65, 0.60)
      .align(s_main["a"])
      .f(pm[1])
      .translate(-20, 14)
    )
    composition += stat_block_frame

    s_stat_block = Scaffold(
        stat_block_frame.bounds().r
        .inset(0.15*stat_block_frame.bounds().r.w)
        .offset(0, -12)
    ).numeric_grid(2,3)

    stat_block = (P([

        (

            # stat name
            StSt(k.title(), deco_fonts[1], 65,
              fit=s_stat_block[i].r.w*0.5,
              wght=0.3,
              wdth=1.0,
            )
            .f(pm[3])
            .align(s_stat_block[i], "C")
            .translate(0, 55)
            ,

            # stat value
            StSt(str(v), deco_fonts[1], 110)
            .f(pm[-2])
            .align(s_stat_block[i], "C")
            .translate(0, -30)
            ,
        )

        for i, (k, v) in enumerate(character["stats"].items())
      ])
      .translate(+12, 0)
    )
    composition += stat_block

    #-------------------------------------------------------------------------
    s_profile = Scaffold(s_main["b"].r.inset(100)).cssgrid("a", "10% 45% a", "a / b / c")
    composition.insert(1,
        StSt("U", containers, 100).align(s_profile)
        .scale(5.05, 7.40)
        .f(pm[1])
    )
    # name
    name = (
        StSt(character["name"], deco_fonts[3], 225,
          wght=1.00,
          tu=65,
        )
        .scale(1.00,1.00)
        .fssw(pm[-2],pm[-2],5)
        .align(s_profile["a"], "C")
    )
    composition += name

    # class
    character_class = (
        StSt(f"{character['class']} lvl {character['level']}", deco_fonts[1], 100,
          wght=0.29,
          fit=s_profile["b"].r.w*1.30,
          tu=51,
        )
        .f(pm[-2])
        .align(s_profile["b"], "C")
    )
    composition += character_class

    # blurb
    lorem = TextLorem(srange=(5,6), prange=(5,5))
    blurb = (
        StSt(lorem.paragraph(), sans_fonts[2], 37,
          wght=0.50,
        )
        .linebreak(s_profile["c"].r.w*1.3)
        .stack("100%")
        .f(pm[-2])
        .align(s_profile["c"], "C")
    )
    composition += blurb

    #-------------------------------------------------------------------------
    portrait_frame = (
      SkiaImage(portrait_frame_filename)
      .ch(potrace(f.a.r.inset(-1000)))
      .scale(0.45)
      .align(s_main["c"])
      .fssw(pm[1],pm[1],1)
      .yalign(character_class.bounds(), "mdy")
    )
    portrait_frame_fill = (P()
      .oval(portrait_frame.bounds().inset(5))
      .f(pm[3])
      .translate(7, -2)
    )
    composition += portrait_frame_fill
    composition += portrait_frame

    composition += (
        P([
        StSt(f'"{lorem.sentence()}"', sans_fonts[2], 32,
          wght=0.60,
        )
        .linebreak(portrait_frame.bounds().r.w*0.8)
        .stack("100%")
        ,

        StSt(f' — {character["name"]}', sans_fonts[2], 32,
          wght=0.60,
        )
        ])
        .xalign(portrait_frame.bounds().r, "E")
        .stack("20%")
        .f(pm[1])
        .align(portrait_frame.bounds().r.offset(0, -0.20*portrait_frame.bounds().r.h), "S")
        ,
    )

    #-------------------------------------------------------------------------
    # palette preview
    composition += pm.preview(f.a.r.take(0.03, "E"), font_size=0)

    composition = composition.ch(temp(0.00))

    return composition
