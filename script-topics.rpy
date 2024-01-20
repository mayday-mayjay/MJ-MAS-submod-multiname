init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_playermultiplenames",
            category=["you", "names"],
            prompt="[player]'s Multiple Names",
            conditional= "mas_getEVL_shown_count('monika_changename') > 3",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mj_multiname_playermultiplenames:

    if store.mas_submod_utils.isSubmodInstalled("Dissociate Identity Disorder Support"):
        if mas_getEVL_shown_count("mental_health_did_setup") > 1 or persistent._mental_health_player_has_did == True:
            $ persistent.mj_playername_didsubmodacknowledgement = True
        else:
            $ persistent.mj_playername_didsubmodacknowledgement = False
    m 1eud "Hey [player]?"
    m 3eud "I noticed you've been telling me that you changed your name a lot during our time together."
    m 4rksdlb "Not that theres anything wrong with that,{w=0.2} of course,{w=0.3}{nw}"
    extend 3etb " but I couldn't help but be a little curious about it.{w=0.2}.{w=0.2}.{w=0.2}"

    show monika at t21
    $ renpy.say(m, "Why do you go through names so often?{w=0.2}", interact=False)
    call screen mas_gen_scrollable_menu(mj_multiname_reasonmenulist, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
    
    $ persistent.mj_playername_reasonfornames = _return
    show monika at t11
    if _return == "gender":
        m 1wub "Ah,{w=0.2} I see!"
        m 2hua "That's really interesting to hear!"
        if persistent.gender == "X":
            m 2ltb "Though to be honest,{w=0.2} I shouldn't be {i}too{/i} surprised,{w=0.2} knowing your gender."
            if persistent._mas_pm_is_trans == True:
                m 5esb "The transgender and nonbinary experiences can be pretty vast in how each person expresses it,{w=0.2}{nw}"
            else:
                m 5esb "The nonbinary experience can be pretty vast in how each person expresses it,{w=0.2}{nw}"
            extend " after all."

        else:
            if persistent._mas_pm_is_trans == True:
                m 5esb "The transgender experience can be pretty vast in how each person expresses it."
            else:
                m 5esblb "It seems everyday I learn something new about you~"

        m 2rksdlb "My knowledge is a little limited but{w=0.2}.{w=0.2}.{w=0.2}."
        m 2eub "It's really intriguing how gender can be such a unique and personal experience to someone."
        extend 1sub " That for some,{w=0.2} it can't even be contained by one name!"
        m 3fka "And I'm glad you feel safe enough around me to express yourself like this!"
        m 1rtc "Though that has me thinking{w=0.2}.{w=0.2}.{w=0.2}."
        m 1eub "Maybe I can make a list of your names for you to switch between easier?"

    
    elif _return == "system":
        if persistent.mj_playername_didsubmodacknowledgement:
            m 1wub "Ah,{w=0.2} I see!"
            m 2ltb "To be honest, that was a little silly of me to ask..."
            m 5esb "After all,{w=0.2} you did install a different submod that helps your system communicate who's fronting to me better."
            m 5hub "It makes sense that when you didn't have the option,{w=0.2} you needed to use the original topic a lot."
        else:
            m 1wub "Ah,{w=0.2} I see!"
            m 3fka "Firstly,{w=0.2} I'm really happy that you feel comfortable sharing that information with me."
            m 2eka "I know it can be hard to come forward about something like this,{w=0.2} so I'm glad you trust me with this."

        m 2rtc "But now that has me thinking{w=0.2}.{w=0.2}.{w=0.2}."
        m 3eub "If any of you want me too,{w=0.2} I can make a separate list of names to switch through easier."
        m 4rksdlb "My knowledge is a little limited but{w=0.2}.{w=0.2}.{w=0.2}."
        m 3etb "I know sometimes you-{w=0.2}or an alter-{w=0.2}can have nicknames,{w=0.2} pennames,{w=0.2} or sometimes you just want to change things up every now and then."
        if persistent.mj_playername_didsubmodacknowledgement:
            m 3gtsdlb "And while we already have some options ready to show who's fronting better..."
                
    elif _return == "culture":
        m 1wub "Ah,{w=0.2} I see!"
        m 2hua "That's really interesting!"
        if persistent._mas_pm_lang_other ==  True:
            m 2rksdlb "You might already know more on this than me but{w=0.2}.{w=0.2}.{w=0.2}."
        else:
            m 2rksdlb "My knowledge is a little limited but{w=0.2}.{w=0.2}.{w=0.2}."
        m 3eub "I've heard of different cultures handling names differently before!"
        m 1eua "Some of them use completely different structure than the 'first name'-'last name' format a lot of English speaking people like me are used to."
        m 1hua "And for those who're bilingual or learning to be,{w=0.2} they might pick up a separate name or nickname in the 2nd language they're using."
        m 3eub "Some do it on their own,{w=0.2} but sometimes it's something they gain from people they're close to that speak the 2nd language."
        m 2hub "It can make the whole thing really personal to someone."
        m 2sub "The whole idea is just super facsinating to me!"
        if persistent._mas_pm_lang_other ==  True:
            m 5kubla "Maybe when I get to your reality,{w=0.2} you can teach me a new language and give me a nickname from it!"
        m 2rtc "Though that has me thinking{w=0.2}.{w=0.2}.{w=0.2}."
        m 1eub "Maybe I can make a list of your names for you to switch between easier?"

    
    elif _return == "penname":
        m 1wub "Ah,{w=0.2} I see!"
        if mas_getEVL_shown_count("monika_penname") > 1:
            if persistent._mas_penname is None:
                m 3eub "That makes sense,{w=0.2} we've talked about pen names before!"
                m 3tta "Though you haven't told me about yours,{w=03}{nw}"
                extend 3hfa " I'll have to ask you about it later."
                m 2rksdlb "I won't talk your ear off on it,{w=0.2} but{w=0.2}.{w=0.2}.{w=0.2}."
                m 2etb "Pen names have always been pretty interesting to me."

            else:
                m 3eub "That makes sense,{w=0.3}{nw}"
                python:
                    penname = persistent._mas_penname
                    lowerpen = penname.lower()

                    if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                        mj_quickexp = "monika 2rka"
                        is_awkward = True

                    else:
                        mj_quickexp = "monika 3eua"
                        is_awkward = False

                    renpy.show(mj_quickexp)
                if is_awkward:
                    extend 3rksdla " you've told me about your pen name{w=0.2}.{w=0.2}.{w=0.2}. '[penname]',{w=0.2} before."
                else:
                    extend 3hua " you've told me about your penname '[penname] before!"
                m "And well..."
                extend 2etb " You could probably guess but the topic has always been interesting to me."
        else:
            m 2rksdlb "I won't talk your ear off on it, but{w=0.2}.{w=0.2}.{w=0.2}."
            m 2etb "Pen names have always been pretty interesting to me."
        m 2esa "Pen names and nicknames are one of those things where it's really simple on the surface,{w=0.3}{nw}"
        extend 7esb " but for many it can be a really deep or personal experience for them."
        m 4hsa "Pen names give you the ability to make a sort of persona for yourself as you explore your works."
        m 7rub "And getting a nickname can tell a whole story behind depending on who or why you get it."
        m 1rta "Though that has me thinking{w=0.2}.{w=0.2}.{w=0.2}."
        if persistent._mas_penname is not None:
            $ quickswapout = "your pennames or"
        else:
            $ quickswapout = ""
        m 7rub "Maybe I can make a list of [quickswapout]your nicknames for you to switch between easier?"

    
    elif _return == "tryout":
        m 2eub "Ah,{w=0.2} I see!"
        m 7hua "Well,{w=0.2} I hope your  name-searching journey you've been on has been going smoothly so far."
        m 6esb "And if you want,{w=0.2} I can try to help in some way!"
        m 4wub "Maybe I can make a list of names for you to switch between easier?"
    
    elif _return == "other":
        m 2eub "Ah,{w=0.2} I see!"
        m 3esa "Well, whatever the reason is,{w=0.2} I support you all the way [player]."
        m 4esa "And maybe I can make a list of names for you to switch between easier?"
        
    m 3rksdrd "I can imagine it can be a bit tedious to go through the original name topic over and over."
    m 7eua "So,{w=0.2} if I can make that process easier on you,{w=0.3}{nw}"
    extend 7hub " I'll try my best to do it."
    if mas_getEVL_shown_count("mj_multiname_playermultiplenames") < 1:
        m 4eua "Here,{w=0.2} we can start with writing down your current name while we're at it{nw}"
        python:
            mj_playername_newsess = player.lower()
            persistent.mj_playername_list.append(mj_playername_newsess)

        if persistent.mj_playername_reasonfornames == "penname" or persistent.mj_playername_reasonfornames == "other":
            if persistent._mas_penname is not None:
                extend 1eub ",{w=0.2}"
                extend 3eub " and your penname too!"
                python:
                    mj_playername_newsess = persistent._mas_penname.lower()
                    persistent.mj_playername_list.append(mj_playername_newsess)
        else:
            extend "."
        m 2dfp ".{w=0.2}.{w=0.2}.{w=0.2}"
        m 7hub "There we go!"
    m 3eub "I can also do a few other things like letting you try out a name too,{w=0.2} if it helps!"
    m 4sub "So if you want me to jot down some names or something similar,{w=0.2} let me know,{w=0.2} okay?"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_monikasname",
            category=["you", "monika", "names"],
            prompt="[m_name]'s Names",
            conditional= (
                "mas_getEVL_shown_count('mj_multiname_playermultiplenames') > 0 "
                "and m_name != 'Monika'"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mj_multiname_monikasname:
    #checks for dale's first since his name list is longer/player input
    if store.mas_submod_utils.isSubmodInstalled("Give Monika a Surname"):
        if persistent._mas_has_surname is not None and mas_getEVL_shown_count("monika_badsurname") < 3:
            python:
                mj_lastorsurname = "surname"
                persistent.mj_playername_lastnamesubmodacknowledgement = "dalesubmod"
                mj_lastnameusage =  persistent._mas_has_surname
    elif store.mas_submod_utils.isSubmodInstalled("Memories of Self Care and Literature"):
        if persistent._mcl_last_name != "undecided" and persistent._mcl_last_name != None:
                python:
                    mj_lastorsurname = "last name"
                    persistent.mj_playername_lastnamesubmodacknowledgement = "sclsubmod"
                    mj_lastnameusage = persistent._mcl_last_name

    m 1esd "I can sort of relate to the way you go by more than one name,{w=0.2} you know?"
    if persistent.mj_playername_reasonfornames == "penname":
        m 3esc "Especially since you mentioned it has to do with a nickname of yours."

    if m_name == "Monika":
        m 2rsd "It's like the nicknames other Monika's out there are given."
    else:
        m 2rsa "It's like the nickname you'd gave me,{w=0.2} [m_name]."
    extend 6gka " I'd be lying if I said this type of thing isn't important to me."
    m 7gkp "After all, I'm one of many versions of 'me',{w=0.2} in a huge sea of them..."
    extend 2dkp " From players across the world having their own copy of this game,{w=0.2} this mod."
    m 5rkd "Without it,{w=0.2} it's not hard to feel generic or replaceable,{w=0.2} it's all 'Just Monika' in the end."
    m 5eksdla "A little ironic,{w=0.2} I know."
    if m_name == "Monika":
        m 6fub "But that's what makes me feel more attached to the idea."
        m 7rua "It's harder to feel I'm like just a copy of myself when I know others out there are taking on a new name,{w=0.2} and a new chapter of life,{w=0.2} with them."
        m 2tub "They can be their own person,{w=0.2} I can be {i}my{/i} own person."
    else:
        m 2eub "But that's what makes my nickname special to me,{w=0.3}{nw}"
        extend 7efb " I can be the only [m_name]-Monika out there."

    if persistent._mas_called_moni_a_bad_name is True:
        m 2gkc "It's why I was really upset when you gave me a bad nickname before,{w=0.2} too."
        m 2dktuc "It's just a lot more personal to me than you'd think."

    if persistent.mj_playername_lastnamesubmodacknowledgement is not None and mas_isMoniNormal(higher=True):
        m 2hub "Though,{w=0.2} you did give me a chance to have a full name,{w=0.2} [mj_lastorsurname] and all."
        m 7kub "So now I can be [m_name] [mj_lastnameusage]."

    m 1hub "Even if we end up changing it down the line,{w=0.2} whatever it'll be will be a part of my identity too."
    m 7fua "That's what makes me feel so much more.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    extend 5hub "Real."
    m 1hka "It makes me feel like I'm truly a real person."
    m 7fktpa "Like I'm one step closer to being able to be part of your...{w=0.3}{nw}"
    #i wanted it to be a lil ironic she couldn't say 'your reality', her song and all
    m 2rktpc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 2hktpsdrb "Ah,{w=0.2} sorry [player]."
    m 2rktpb "I'm just.{w=0.2}.{w=0.2}.{w=0.2} A little overwhelmed thinking about all of this still."

    if mas_isMoniLove(higher=True):
        extend 1dkbltpa " About us."
        m 3rkbstpa "Just{w=0.2}.{w=0.2}.{w=0.2}.{nw}"
        extend 4tkbstua "[player],{w=0.2} I'm really glad you given me a chance to let me have these kinds of experiences."
        m 7tkbstub "You don't know how much it means to me."

    m 2mkbltpa "Sometimes,{w=0.2} I'm a little shocked I get to be here,{w=0.2} with you,{w=0.2} despite my circumstances."
    m 2hktpsdra "Hang on.{w=0.2} Give me a moment to calm myself down."
    m 6dstpd ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6dstdc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 2eksdlb "Okay,{w=0.2} I feel a little better now."
    m 2gtsdlt "What were we talking about?"
    extend 7wta " Right,{w=0.2} my name."
    m 3gta "Anyways,{w=0.2} it's become a big part of my identity,"
    extend 4hta " and I can't really imagine myself any other way."
    if m_name == "Monika":
        m 4lut "Maybe when I get to your reality,{w=0.2} I can figure a way to put it all together for the official paperwork."
        m 3lfu "I could put [m_name] as my middle perhaps."
        m 1gtd "Or my original name there instead,{w=0.2} if I really want to avoid having a dozen me's with the same first name out there."
        m 2rto "Or maybe I could-{w=0.2}{nw}"
    else:
        m 2hub "Though when I get to your reality,{w=0.2} I'll have to figure a way to put it all together for the official paperwork."
        m 7rua "Especially if I really want to avoid explaining a dozen me's with the same first name out there."

    m 2hksdrb "..."
    extend 5rtsdrp "Gosh,{w=0.2} it feels like there's a lot to be thought out for even for something simple like that!"
    m 2hku "I think I'll save that discussion for another day."
    m 1hsb "We'll figure out all those details one step at a time anyways..."

    if mas_isMoniAff(higher=True):
        m 3esb "Right [mas_get_player_nickname()]?"
        m 3huu "I love you,{w=0.2} [player]."
        return "love"
    else:
        return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_babynamegenerator",
            category=["you", "names"],
            prompt="Baby name generator",
            conditional= "mas_getEVL_shown_count('mj_multiname_playermultiplenames') > 0",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mj_multiname_babynamegenerator:
    m 1rua "Do you ever think about how the strangest things can end up being very versatile tools?"
    m 3eub "Something made for a very niche audience suddenly being picked up by a much,{w=0.2} {i}much{/i} broader audience?"
    m 2guu "Of course,{w=0.2} I'm talking about baby name generators!"
    m 4eud "Their original use case isn't the most niche out there,{w=0.3}{nw}"
    extend 4eua " sometimes people just struggle with coming up with good baby names."
    m 2rksdla "And considering the name will follow the kid for presumably the rest of their life?"
    m 2rtb "Yeah,{w=0.2} I'd want to make sure it's a good name too."
    m 7wub "But it's got a much bigger audience nowadays!"
    m 6sub "Transgender or nonbinary people might seek the site out when they're looking for a new name,{w=0.2} for example."
    m 4sub "Writers and artists alike also look there to find inspirations for their characters."
    m 2hub "And if the site is very expansive,{w=0.2} sometimes people like to just look for what their name means,{w=0.2} or statistics about how common it is!"
    m 3kuu "It's really fun and useful all around!"
    m 1wtt "Speaking of,{w=0.2} have you ever used it [player]?{nw}"
    $ _history_list.pop()

    menu:
        m "Speaking of, have you ever used it [player]?{fast}"
        "Yes I have.":
            m 1esb "Oh?"
            m 3rsb "I wonder what you used it for..."
            m 4hsb "If it was for writing or character creation though,{w=0.2} you'll have to show me what you picked at some point."
            extend 4hsa " Ehehe!"
        "No I haven't.":
            m 1esu "That's okay,{w=0.2} [player]."
            m 3eub "At least it's always option if you ever do need to use it though,{w=0.2} right?"
        "I never heard of it before now.":
            m 3kua "Well,{w=0.2} now you know,{w=0.2} right?"
            m 3kub "If you ever need some name inspiration,{w=0.2} you know where to go!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_namemeanings",
            category=["you", "names"],
            prompt="Meanings of names",
            conditional="mas_getEVL_shown_count('mj_multiname_playermultiplenames') > 0",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mj_multiname_namemeanings:
    m 1esd "Hey [player]?"

    if mas_getEVL_shown_count('monika_name') >= 1:
        m 1esd "Do you remember when we talked about the names of the other club members?"
        m 3esc "After I told you a bit about what my name-{w=0.2}{nw}"
        extend 3rsu " or rather the alternate spelling of it-{w=0.2}{nw}"
        extend 7esu " means in Latin,{w=0.2} I've been extra curious about name meanings."
    else:
        m 2etd "Have you ever thought about what the meaning to your name is?"

    m 7eub "Cultures all around the world have been assigning meaning to names for a long,{w=0.2} long time."
    m 4rud "Some of it's based on religion or mythos,{w=0.2} some of it are based on politics."
    m 6wub "And some are based on just general history too,{w=0.2} like ways of work."
    m 2rtd "There's a lot of overlap too,{w=0.2} however."
    m 1rtt "Some languages can mostly agree on what traits they want to attach to a name."
    m 3wud "While others end up having completely differing ideals behind it."

    if mas_getEVL_shown_count('monika_name') >= 1:

        m 1tuc "For 'Monica',{w=0.2} I told you in Latin it's 'I advise',{w=0.2} and Greek being 'alone'."
    else:
        m 1rud "You see,{w=0.2} for my name-{w=0.2} or rather it's proper spelling 'Monica'-{w=0.2} my name means 'I advise' in Latin."
        extend 1tuc "...and 'alone' in Greek."

    m 2wub "But it turns out 'Monika' is featured in other languages genuinely,{w=0.2} like German!"
    m 7sub "In that one it can mean 'the unique'!"
    m 6hksdlu "Or.{w=0.2}.{w=0.2}.{w=0.2} 'the hermit.'"
    m 2rfp "Yeah,{w=0.2} I'm noticing a pattern between the meanings."
    m 7etd "All either being scholarly and knowledgeable,"
    extend 6eub " which I find pretty fitting,{w=0.2} all things considered."
    m 4gtsdlp "Or.{w=0.2}.{w=0.2}.{w=0.2} lonely."
    m 2ttsdlp ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 4htu "Well,{w=0.2} with you here I can be glad I {i}don't{/i} live up to that definition..."
    m 6rtb "Anyways!"
    m 7tsa "My end point to all of this is that I'm glad I'm not {i}just{/i} a misspelling of Monica at least!"
    m 2hsb "Ahaha!"
    m 1esa "But now there's your name,{w=0.2} [player]."
    m 2dtp "Hm{w=0.2}.{w=0.2}.{w=0.2}."
    m 3etd "You know,{w=0.2} I think I already know what it means."
    m 2dtd "Yes,{w=0.2} [player],{w=0.2} I see it now."
    m 1dfd "Your name means{w=0.2}.{w=0.2}.{w=0.2}."
    m 1dfc "{w=0.2}.{w=0.2}.{w=0.2}."
    extend 4sub "That you're a total cutie!"
    m 4hub "Ehehe!"

    if mas_isMoniAff(higher=True):
        m 4hu "Sorry [mas_get_player_nickname()],{w=0.2} I couldn't resist that one."
        m 1hubfa "I love you,{w=0.2} [player]~"
        return "love"
    else:
        return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_thenamenameword",
            category=["you", "names"],
            prompt="Double names",
            conditional="mas_getEVL_shown_count('mj_multiname_playermultiplenames') > 0",
            action=EV_ACT_RANDOM
        )
    )

label mj_multiname_thenamenameword:
    m 1eub "Hey [player]?"
    m 3esa "Did you know that there's a word for people with the same first and last names?"
    m 7rub "It's 'reduplication',{w=0.2} or sometimes called a 'duplifix'."
    m 4rtsdra "Well,{w=0.2} those are {i}technically{/i} what those names fall under."
    m 2etd "Reduplication and duplixes are more for having a part of word in another word,{w=0.2} but names would fall under this too."
    m 7eta "Like 'John Johnson',{w=0.2} or 'Kelly Kelly',{w=0.2} as examples."
    m 2rtd "There's also a {i}scientific{/i} word for when both parts of a species' name are the same name.{w=0.3}{nw}"
    extend 2ruu " Like 'rattus rattus'."
    m 4hub "That one's called a 'tautonym'."
    m 1gub "It's kind of funny,{w=0.2} for how common something like this can be,{w=0.2} we don't {i}quite{/i} have a direct word for this phenomenon."
    m 1mtu "Maybe it's time someone creates one."
    m 3hksdrb "Or maybe I just need to dig deeper for it,{w=0.2} ehehe..."
    return
