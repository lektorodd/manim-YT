from manim import *
import numpy as np

class Intro(Scene):
    def construct(self):
        # videotittel
        tittel = Text(
            "MONOTONIEIGENSKAPAR",
            font = "Inter",
            weight="HEAVY"
        )

        tittel.width = config["frame_width"] - 4

        # nettstad 
        lektorodd = Text(
            "lektorodd.github.io",
            font = "JetBrains Mono",
        )

        lektorodd.width = config["frame_width"] - 10
        lektorodd.next_to(tittel, 2*DOWN)

        # SoMe - GH og YT
        brukarnamn = Text("lektorodd", font="JetBrains Mono")

        gh_logo = VGroup(
            SVGMobject("./img/github.svg", fill_color=WHITE).scale(0.4), 
            brukarnamn.copy()
        ).arrange(RIGHT, buff=0.4)

        yt_logo = VGroup(
            SVGMobject("./img/youtube.svg", fill_color=WHITE).scale(0.3),
            brukarnamn.copy()
        ).arrange(RIGHT, buff=0.4)

        some = VGroup(gh_logo, yt_logo).arrange(DOWN, buff=0.4).next_to(tittel, 2*DOWN) #.to_corner(DR, buff=0.05).scale(0.5)
        some.target = some.copy().scale(0.3).to_corner(DR, buff=0.4).set_opacity(0.5)

        # Animerer
        self.play(Write(tittel, run_time=1.5))
        self.wait(0.5)
        self.play(DrawBorderThenFill(some, run_time=0.7))
        self.wait(3)
        self.play(
            ReplacementTransform(some, some.target),
            Write(lektorodd, run_time=0.7)
        )
        self.wait()
        self.play(FadeOut(tittel), FadeOut(lektorodd))
        self.wait()
        self.play(FadeOut(some.target))
        self.wait()

class Monotoni(Scene):
    def construct(self):
        # videotittel
        tittel = Text(
            "MONOTONIEIGENSKAPAR",
            font = "Inter",
            weight="HEAVY"
        )

        tittel.width = config["frame_width"] - 6

        # monotoni - 0-7
        mono = Text(
            "MONOTONIEIGENSKAPAR", 
            font="Inter", 
            weight="HEAVY",
            t2c={"MONOTONI": YELLOW}
            )

        mono.width = config["frame_width"] - 6

        self.play(Write(tittel), run_time=0.5)
        self.wait()
        self.play(ReplacementTransform(tittel, mono))
        self.wait()

        # pil 
        pil = CurvedArrow([-2.5,-0.5,0], [-1.5,-1.5,0], angle=TAU/5, color=YELLOW)
        self.play(Create(pil))

        bilde = ImageMobject("./img/monotoni.png").scale(0.3).next_to(pil, RIGHT, buff=0.5).shift(DOWN)
        self.play(FadeIn(bilde))
        self.wait(3)

        # renske opp...
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait()


class Graf(MovingCameraScene):
    def construct(self):
        
        # Lager akseobjekt
        akser = Axes(
            x_range=[-1, 9],
            y_range=[-4, 5],
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False
            },
        )

        # lagar ein funksjon
        def f(x):
            return 1/10 * x * (x-2) * (x-4) * (x-7) + 1

        # ekstremalpunkt og merkelappar på rett plass...
        ekstremalpunkt = [0.776336, 3.03830, 5.93536]
        labels = ["a", "b", "c"]

        ekstremalpunkt_labels = [
            Tex(label).next_to(
                akser.c2p(x, 0), 
                UP
            ) if label == "a" or label == "c" else Tex(label).next_to(
                akser.c2p(x, 0), 
                DOWN
            )
            for x, label in zip(ekstremalpunkt, labels)
        ]

        # plottar funksjonen
        f1 = akser.plot(f,x_range=[-1, 9], color=BLUE)

        # plottar segment av funksjonen i ulike fargar (etter monotoni)
        f2 = akser.plot(f, x_range=[-1, ekstremalpunkt[0]], color=RED, stroke_width=5)
        f3 = akser.plot(f, x_range=[ekstremalpunkt[0], ekstremalpunkt[1]], color=GREEN, stroke_width=5)
        f4 = akser.plot(f, x_range=[ekstremalpunkt[1], ekstremalpunkt[2]], color=RED)
        f5 = akser.plot(f, x_range=[ekstremalpunkt[2], 9], color=GREEN)

        # lagar vt for å endra x-verdi
        vt = ValueTracker(-1)

        # Lagar ein prikk som føl grafen
        prikk = Dot(color=YELLOW).move_to(
            akser.c2p(vt.get_value(), f(vt.get_value()))
        )

        # flyttar prikk etter valuetrackeren
        prikk.add_updater(lambda m: m.move_to(
            akser.c2p(vt.get_value(), f(vt.get_value()))
        ))

        # viser fuksjon og aksar
        self.play(Create(akser))
        self.wait(1)
        self.play(Create(f1, run_time=4))

        # Legge til stipla linje frå x-akse til ekstremalpunkt
        for x in ekstremalpunkt:
            linje = DashedLine(
                akser.c2p(x, 0),
                akser.c2p(x, f(x)),
                color=WHITE
            )
            ep = Dot(color=WHITE).move_to(akser.c2p(x, f(x)))
            self.play(Create(linje), run_time=0.3)
            self.wait(0.5)
            self.play(Create(ep), run_time=0.3)

        # Legg inn prikk og ekstremalpunkt_labels
        self.play(Write(VGroup(*ekstremalpunkt_labels)))
        self.wait(1)
        self.add(prikk)
        self.wait(1)

        # Animerer prikken
        self.play(vt.animate.set_value(ekstremalpunkt[0]), run_time=3)
        self.add(f2)
        self.wait()
        self.play(vt.animate.set_value(ekstremalpunkt[1]), run_time=3)
        self.add(f3)
        self.wait()
        self.play(vt.animate.set_value(ekstremalpunkt[2]), run_time=3.5)
        self.add(f4)
        self.wait()
        self.play(vt.animate.set_value(8), run_time=4.5)
        self.add(f5)
        self.wait(1)

        # tilbakestiller vt
        vt.set_value(-1)

        # Dynamisk tangentlinje som oppdateres basert på ValueTracker
        tangent = always_redraw(lambda: akser.get_secant_slope_group(
            x=vt.get_value(),
            graph=f1,
            dx=0.001,
            secant_line_length=4,
            secant_line_color=YELLOW,
        ))

        # Animerer tangenten
        self.add(tangent)
        self.wait(1)
        self.play(vt.animate.set_value(ekstremalpunkt[0]), run_time=3)
        self.wait()
        self.play(vt.animate.set_value(ekstremalpunkt[1]), run_time=3)
        self.wait()
        self.play(vt.animate.set_value(ekstremalpunkt[2]), run_time=3.5)
        self.wait()
        self.play(vt.animate.set_value(8), run_time=4.5)
        self.wait()
        self.wait(1)

        self.remove(tangent, prikk)
        self.wait(1)

        # Legger til tekst
        vekst1 = Tex("Strengt voksande", font_size=32).shift(2*UP)
        vekst2 = MathTex(r"x_1 < x_2 \Leftrightarrow f(x_1) < f(x_2)", font_size=32).next_to(vekst1, DOWN)   

        vekst3 = Tex("Strengt avtagande", font_size=32).next_to(vekst2, DOWN).shift(0.2*DOWN)
        vekst4 = MathTex(r"x_1 < x_2 \Leftrightarrow f(x_1) > f(x_2)", font_size=32).next_to(vekst3, DOWN)
        
        strengt_voksande = VGroup(vekst1, vekst2)
        strengt_avtagande = VGroup(vekst3, vekst4)

        tekst = VGroup(strengt_voksande, strengt_avtagande)
        tekst.scale(0.7).shift(1.5*UP).to_edge(RIGHT, buff=0.3)

        # flytte inn kamera / zoome inn
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(tekst))
        self.play(Write(strengt_voksande))
        self.wait(3)
        self.play(Restore(self.camera.frame))

        # utheve deler av grafen og formelen
        self.play(Indicate(f3), Indicate(f5), run_time=2)
        self.wait(1)

        # plotte punkt funksjon
        def plotteToPunkt(x1, x2):
            # Linjer til aksane frå punkta
            linje1 = DashedLine(akser.c2p(x1, 0), akser.c2p(x1, f(x1)), color=WHITE, stroke_width=3)
            linje2 = DashedLine(akser.c2p(x2, 0), akser.c2p(x2, f(x2)), color=WHITE, stroke_width=3)
            linje3 = DashedLine(akser.c2p(0, f(x1)), akser.c2p(x1, f(x1)), color=WHITE, stroke_width=3)
            linje4 = DashedLine(akser.c2p(0, f(x2)), akser.c2p(x2, f(x2)), color=WHITE, stroke_width=3)

            punkt1 = Dot(akser.c2p(x1, f(x1)), color=RED)
            punkt2 = Dot(akser.c2p(x2, f(x2)), color=RED)

            px1 = VGroup(linje1, linje3, punkt1)
            px2 = VGroup(linje2, linje4, punkt2)

            # Merkelappar til x1, x2, f(x1) og f(x2)
            fonstrl = 18
            x1_label = MathTex("x_1", font_size=fonstrl).next_to(linje1, DOWN, buff=0.3)
            x2_label = MathTex("x_2", font_size=fonstrl).next_to(linje2, DOWN, buff=0.3)
            f1_label = MathTex("f(x_1)", font_size=fonstrl).next_to(linje3, LEFT)
            f2_label = MathTex("f(x_2)", font_size=fonstrl).next_to(linje4, LEFT)

            merker = VGroup(x1_label, x2_label, f1_label, f2_label)

            # Animerer
            self.play(self.camera.frame.animate.scale(0.5).to_edge(LEFT, buff=0.5))
            self.play(Create(px1), Create(px2))
            self.play(Write(merker))
            self.wait(2)
            self.play(Restore(self.camera.frame))
            self.wait(2)
            self.play(FadeOut(px1), FadeOut(px2), FadeOut(merker))

        # Lage to punkt x1 og x2 og vise at f(x1) < f(x2)
        x1, x2 = 2, 2.5
        plotteToPunkt(x1, x2)
  
    
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(tekst))
        self.play(Write(strengt_avtagande))
        self.wait(3)
        self.play(Restore(self.camera.frame))

        # Lage to punkt x1 og x2 og vise at f(x1) < f(x2)
        x1, x2 = .1, .7
        plotteToPunkt(x1, x2)

        self.play(Indicate(f2), Indicate(f4), run_time=2)
        self.wait(1)

        self.play(FadeOut(tekst))
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [akser, f1]]
            # All mobjects in the screen are saved in self.mobjects
        )

        self.wait()

class Forteiknslinjer(Scene):
    def construct(self):

        start = -1
        slutt = 9
        # Lager akseobjekt
        akser = Axes(
            x_range=[start, slutt],
            y_range=[-4, 5],
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False
            },
        )

        # lagar ein funksjon
        def f(x):
            return 1/10 * x * (x-2) * (x-4) * (x-7) + 1

        # plottar funksjonen
        f1 = akser.plot(f,x_range=[-0.52, 7.32], color=BLUE)

        startbakgrunn = VGroup(akser, f1)

        # legg til på scenen
        self.add(startbakgrunn)

        akser2 = akser.copy().set_y_length(4).scale(0.8).to_edge(UP, buff=0.5)
        funksjon = akser2.plot(f, x_range=[-0.52, 7.32], color=BLUE)

        self.play(ReplacementTransform(startbakgrunn, VGroup(akser2, funksjon)))

        # nullpunkt
        nullp = [0.219, 1.516, 4.367, 6.898]

        for x in nullp:
            self.play(Create(Dot(akser2.c2p(x, 0), color=WHITE), run_time=0.2))

        self.wait()

        # Forteiknslinje for f(x)
        x_linje = NumberLine(
            x_range=[start, slutt],
            length=akser2.x_length,
            color=WHITE,
            include_numbers=False,
            include_ticks=False,
        ).scale(0.8).next_to(akser2, DOWN, buff=1)

        # mal for forteiknslinje like stor som x-linja
        f_linje = x_linje.copy().shift(DOWN)

        # Pynte litt på x-linja 
        x_linje.add_tip()
        x_linje.set_stroke(width=6)
        
        xmerke = Tex("x").next_to(x_linje, RIGHT, buff=0.2)
        self.play(Write(xmerke))
        self.play(Write(x_linje))
        self.wait()

        labels = ["a", "b", "c", "d"]

        # Nullpunkt linjer nedover
        for x, label in zip(nullp, labels):
            linje = DashedLine(
                akser2.c2p(x, 0),
                x_linje.n2p(x)+0.7*UP,
                color=WHITE
            )
            self.play(Create(linje), run_time=0.4)

            merke = MathTex(label).scale(0.8).next_to(x_linje.n2p(x), UP, buff=0.3)
            
            self.play(Create(merke))
            self.wait(0.2)

        # Ticks 
        ticks_f = VGroup(*[Line(
            x_linje.n2p(x)+0.1*UP,
            x_linje.n2p(x)+0.1*DOWN,
            color=WHITE, stroke_width=5
            ) for x in nullp])

        self.play(Create(ticks_f))
        self.wait(2)

        # Merke på f(x)
        fmerke = MathTex("f(x)").next_to(f_linje, LEFT, buff=0.5)
        self.play(Write(fmerke))

        # Legge til 0 på flinje
        label_nullp = VGroup(*[MathTex("0").move_to(f_linje.n2p(x)) for x in nullp])

        self.play(Write(label_nullp))
        self.wait(2)
        
        # Dei ulike delane av forteiknslinja
        avstd = 0.2
        fl1 = Line(f_linje.n2p(start), f_linje.n2p(nullp[0]-avstd), color=WHITE, stroke_width=4)
        fl2 = DashedLine(f_linje.n2p(nullp[0]+avstd), f_linje.n2p(nullp[1]-avstd), color=WHITE, stroke_width=4)
        fl3 = Line(f_linje.n2p(nullp[1]+avstd), f_linje.n2p(nullp[2]-avstd), color=WHITE, stroke_width=4)
        fl4 = DashedLine(f_linje.n2p(nullp[2]+avstd), f_linje.n2p(nullp[3]-avstd), color=WHITE, stroke_width=4)
        fl5 = Line(f_linje.n2p(nullp[3]+avstd), f_linje.n2p(slutt), color=WHITE, stroke_width=4)
  
        self.play(Create(VGroup(fl1, fl3, fl5)), run_time=4)
        self.wait()
        self.play(Create(VGroup(fl2, fl4)), run_time=2.5)
        self.wait(4)

        # nytt oppsett med xlinja og merker, men tar vekk flinje osv
        self.add(funksjon, akser2, x_linje, xmerke)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [funksjon, akser2, x_linje, xmerke]],
        )
        self.wait()

        # Gjenta men med derivert
        eksp = [0.776336, 3.03830, 5.93536]
        labels = ["a", "b", "c"]

        for x in eksp:
            self.add(Dot(akser2.c2p(x, f(x)), color=WHITE))

        self.wait()

        df_linje = f_linje.copy()

        # Ekstremalpunkt linjer nedover
        for x, label in zip(eksp, labels):
            linje = DashedLine(
                akser2.c2p(x, 0),
                x_linje.n2p(x)+0.7*UP,
                color=WHITE
            )
            self.play(Create(linje), run_time=0.8)

            merke = MathTex(label).scale(0.8).next_to(x_linje.n2p(x), UP, buff=0.3)
            
            self.play(Create(merke))
            self.wait(0.2)

        # Ticks 
        ticks_df = VGroup(*[Line(
            x_linje.n2p(x)+0.1*UP,
            x_linje.n2p(x)+0.1*DOWN,
            color=WHITE, stroke_width=5
            ) for x in eksp])

        self.play(Create(ticks_df))
        self.wait()

        # Lage tangentar
        tangentar = VGroup()

        for x in eksp:
            tangent = akser2.get_secant_slope_group(
                x=x,
                graph=funksjon,
                dx=0.0001,
                secant_line_length=2,
                secant_line_color=YELLOW,
            )
            tangentar.add(tangent)

        # viser tangentar
        self.play(Create(tangentar))

        # Merke på df(x)
        dfmerke = MathTex("f'(x)").next_to(f_linje, LEFT, buff=0.5)
        self.play(Write(dfmerke))

        # Legge til 0 på dflinje
        label_eksp = VGroup(*[MathTex("0").move_to(df_linje.n2p(x)) for x in eksp])
        self.play(Write(label_eksp))
        self.wait(2)

        # ta vekk tangentane
        self.play(Uncreate(tangentar))
        self.wait()

        # Dei ulike delane av forteiknslinja
        avstd = 0.2
        dfl1 = DashedLine(df_linje.n2p(start), df_linje.n2p(eksp[0]-avstd), color=WHITE, stroke_width=4)
        dfl2 = Line(df_linje.n2p(eksp[0]+avstd), df_linje.n2p(eksp[1]-avstd), color=WHITE, stroke_width=4)
        dfl3 = DashedLine(df_linje.n2p(eksp[1]+avstd), df_linje.n2p(eksp[2]-avstd), color=WHITE, stroke_width=4)
        dfl4 = Line(df_linje.n2p(eksp[2]+avstd), df_linje.n2p(slutt), color=WHITE, stroke_width=4)
  
        self.play(Create(VGroup(dfl1, dfl3)), run_time=4)
        self.wait()
        self.play(Create(VGroup(dfl2, dfl4)), run_time=2.5)
        self.wait(4)

        # renske opp...
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait()

        # lage oppsummering
        oppsummering_xlinje = VGroup(x_linje, xmerke, ticks_f, ticks_df).shift(4*UP)
        oppsummering_flinje = VGroup(fl1, fl2, fl3, fl4, fl5, label_nullp).next_to(x_linje,2*DOWN)
        oppsummering_dflinje = VGroup(dfl1, dfl2, dfl3, dfl4, label_eksp).next_to(x_linje, 5*DOWN)

        self.play(Create(oppsummering_xlinje))
        self.play(Write(fmerke.next_to(oppsummering_flinje, LEFT)))
        self.play(Create(oppsummering_flinje))
        self.play(Write(dfmerke.next_to(oppsummering_dflinje, LEFT)))
        self.play(Create(oppsummering_dflinje))
        self.wait()

        # akse for "retningslinjer"
        akser3 = Axes(
            x_range=[start, slutt],
            y_range=[0,1], 
            y_length=2
        ).scale(0.8).next_to(oppsummering_dflinje, DOWN, buff=1.1)

        # "retningslinjene"
        retning = VGroup(
            Line(akser3.c2p(start, 1), akser3.c2p(eksp[0], 0), buff=0.2),
            Line(akser3.c2p(eksp[0], 0), akser3.c2p(eksp[1], 1), buff=0.2),
            Line(akser3.c2p(eksp[1], 1), akser3.c2p(eksp[2], 0), buff=0.2),
            Line(akser3.c2p(eksp[2], 0), akser3.c2p(slutt, 1), buff=0.2)
        ).set_color(YELLOW)

        self.play(ShowIncreasingSubsets(retning), run_time=4)
        self.wait(3)

        # Fadeut alt til slutt. 
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.wait()

