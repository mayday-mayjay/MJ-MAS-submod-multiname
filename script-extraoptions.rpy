## monika picking a name for the player
label mj_playername_pickforplayer:
    #refresh/define these vars/quips rq
    python:
        mj_playername_namepool = []
        mj_playername_randomattempt = ""
        mj_playername_comparisonlist = []
        
        #i went overboard with the list, but at least a big list of names won't have as much repeating quips...
        mj_randomattempt_quips = [
        "I'm feeling like it's a '[mj_playername_randomattempt.capitalize()]' kind of day.",
        "Does '[mj_playername_randomattempt.capitalize()]' sound good to you?",
        "What about '[mj_playername_randomattempt.capitalize()]'?",
        "Let's try '[mj_playername_randomattempt.capitalize()]'!",
        "What's your take on '[mj_playername_randomattempt.capitalize()]'?",
        "How about going with '[mj_playername_randomattempt.capitalize()]'?",
        "Would you consider giving '[mj_playername_randomattempt.capitalize()]' a shot?",
        "May I suggest '[mj_playername_randomattempt.capitalize()]'?",
        "I propose '[mj_playername_randomattempt.capitalize()]'!",
        "I'm leaning towards '[mj_playername_randomattempt.capitalize()]'!",
        "How does '[mj_playername_randomattempt.capitalize()]' feel to you?",
        "My heart says '[mj_playername_randomattempt.capitalize()]'!",
        "My mind says '[mj_playername_randomattempt.capitalize()]'!",
        "My soul says '[mj_playername_randomattempt.capitalize()]'!",
        "What if we took a chance with '[mj_playername_randomattempt.capitalize()]'?"
        ]

    show monika at t11
        
    #quick check if the list is empty/only one option
    if len(persistent.mj_playername_list) == 0:
        m 1rksdla "Well I would,{w=0.2} but{w=0.2}.{w=0.2}.{w=0.2}."
        m 3rksdla "Your name list is empty,{w=0.2} [player]."
        m 1hka "You need to tell me some names to write down before I can pick one."
        
    #check if theres one name in the list and if the players name is the ONLY name in the list
    elif len(persistent.mj_playername_list) == 1:
        m 1rksdla "Well I would,{w=0.2} but{w=0.2}.{w=0.2}.{w=0.2}."
        if player.lower() in persistent.mj_playername_list:
            m 3rksdla "The only name in your list is your own,{w=0.2} [player]."
        else:
            m 3rksdla "There's only one name in the list,{w=0.2} [player]."
        m 1hka "You need to tell me some more names to write down before I can pick one."

        
    else:
        m 1hub "I can do that!"
        m 3eua "Do you want me to pick from a certain pool of names or just your whole list?{nw}"
        # here she does a check list menu to pick names from your list, and THAT list gets used in the loop
        $ _history_list.pop()
        menu:
            m "Do you want me to pick from a certain pool of names or just your whole list?{fast}"
            "From a pool of names.":
                call mj_playername_namepoolpick
                if len(mj_playername_namepool) == 0:
                    return
                else:
                    $ mj_playername_comparisonlist = mj_playername_namepool

            "From my whole list":
                $ mj_playername_comparisonlist = persistent.mj_playername_list
        m 2rtc "Let's see{w=0.2}.{w=0.2}.{w=0.2}."
        call mj_playername_randomplz
    return

label mj_playername_randomplz:
    #name loop
    python:
        mj_namepickingloop = True
        mj_namepickingloop2 = False
        mj_namepicking1sttime = True
        mj_quickrejectednames = []
        
    while mj_namepickingloop:
        m 5rup "Hm{w=0.2}.{w=0.2}.{w=0.2}."     
        call mj_playername_randomplz_randompick
        $ mj_randomattempt_quip = renpy.substitute(renpy.random.choice(mj_randomattempt_quips))
        m 3hub "[mj_randomattempt_quip]{nw}"
        $ _history_list.pop()
        menu: 
            m "[mj_randomattempt_quip]{fast}"
            "Perfect, thanks!":
                ##todo, again checking if the random name is eggable i should maybe do?
                $ persistent.playername = mj_playername_randomattempt.capitalize()
                $ player = mj_playername_randomattempt.capitalize()
                m 2eub "Of course [player]!"
                $ mj_namepickingloop = False
                
            "Eh... Try a different one?":
                #add rejected name to list 
                m 2rtc "Okay,{w=0.2} let's see then."
                $ mj_quickrejectednames.append(mj_playername_randomattempt)
                call mj_playername_randomplz_randompick
                
            "Nevermind, I'm not really feeling it...":
                m 3rksdlb "Ah,{w=0.3}{nw}"
                extend 3hksdlb " that's okay [mas_get_player_nickname()]."
                m 1eka "Maybe next time."
                $ mj_namepickingloop = False
    return

# the actual random picking process, it filters out choices the player already rejects during a full round of listing off names so they arent repeated
label mj_playername_randomplz_randompick:
    #random pick the name
        
    $ mj_namepickingloop2 = True
        
    while mj_namepickingloop2:
        $ mj_playername_randomattempt = renpy.substitute(renpy.random.choice(mj_playername_comparisonlist))
        
        #the first time itll do no checks so just quickly end the loop
        if mj_namepicking1sttime:
            $ mj_namepickingloop2 = False
            $ mj_namepicking1sttime = False
        else:
            #after that it needs to check if the name is already rejected or if monika has run out of options
            if set(mj_quickrejectednames) == set(mj_playername_comparisonlist):
                call mj_playername_randomplz_randompickfail
            elif mj_playername_randomattempt in mj_quickrejectednames:
                pass
            else:
                $ mj_namepickingloop2 = False
    return
    
# if the player goes through all availiable names and didnt pick one itll end up here and end the interaction
label mj_playername_randomplz_randompickfail:
    m 1rksdla "Uh{w=0.2}.{w=0.2}.{w=0.2}. [player]?"
    m 3rksdlb "We've gone through all your options and you didn't seem keen on any of them..." 
    m 3ekc "I don't think I can be the one to pick a name for you."
    m 2eka "Sorry I can't help you more with your indecisiveness on this one but{w=0.2}.{w=0.2}.{w=0.2}."
    $ mj_namepickingloop2 = False
    $ mj_namepickingloop = False
    return
    
    
## a menu for when the player just wants to select through some of the names available

label mj_playername_namepoolpick:
    
    #quick check if the list only has 2 options [since theres no point in picking a pool then]
    if len(persistent.mj_playername_list) == 2:
        m 1rksdla "Well,{w=0.2} there's not a lot of options to pick from [player]{w=0.2}.{w=0.2}.{w=0.2}."
        m 1eua "I'll just pick between these two names that are here."
        $ mj_playername_namepool = persistent.mj_playername_list
    else:
        m 3hua "Of course!"
        $ mj_namepoolpicking = True
        while mj_namepoolpicking:
            #make the menu-ready tuple list from the player's names in alphabetical order
            python:
                mj_playername_namepool = []
                mj_playername_tuplelist = []
                persistent.mj_playername_list.sort()
                for mj_playername in persistent.mj_playername_list:
                    mj_playername_tuplelist.append((mj_playername.capitalize(), mj_playername, False, True, False))
        
            show monika at t21
            python:
                renpy.say(m, "Select which names you want me to pick from.", interact=False)
                mj_playername_didplayerchoosenames = False

            #the menu, a checklist
            call screen mas_check_scrollable_menu( \
                mj_playername_tuplelist, \
                mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, \
                selected_button_prompt=_("Done."), default_button_prompt=_("Done."), \
                return_all=True)
            
            #every item the player selects will be added to the list, and a flag will be set for a quick 'done' dlg
            python:
                for mj_playernameitem, mj_playernameadditem in _return.items():
                    if mj_playernameadditem is True:
                        mj_playername_namepool.append(mj_playernameitem)

            #some quick checks if there's not enough names to randomize
            if len(mj_playername_namepool) == 0:
                m 2etc "Hm?{w=0.2} Changed your mind [player]?"
                m 1eka "Well,{w=0.2} let me know if you want to do this later,{w=0.2} okay?"
                $ namepoolpicking = False
            elif len(mj_playername_namepool) == 1:           
                m 1hka "You need to give me more names than that [player]{w=0.2}.{w=0.2}.{w=0.2}."
                m 1eka "Try again."
            else:                
                show monika at t11
                m 1hub "Okay!"
                $ mj_namepoolpicking = False
    return
    
##deals with an enter loop, again, but different for the 'try on a name' option
label mj_playername_enterloop_tryname(mj_inputprompt):
    #get players input to compare to reactions, if it passes the reaction it gets tried on + it doesn't skip loop dlg
    python:
        done1 = False 
        mj_playername_attempt = ""
        mj_playername_monikareaction = False
        mj_playername_playergoofednamemaking = False
        
        good_quips = [
            "That's a wonderful name!",
            "I like that a lot, [player].",
            "I like that name, [player].",
            "That's a great name!"
        ]
        #why isn't basemod good quips defined in the same place as the other quips??? 
    
    while done1 is False:    
        python:
            mj_playername_skiploopdlg = False
            mj_playername_attempt = mas_input(
                "[mj_inputprompt]",
                length=20,
                screen_kwargs={"use_return_button": True}
        ).strip(' \t\n\r')
        
        #####reactions to no input/cancel/same name/preexisting name and bad/awk/good names
        if mj_playername_attempt == "cancel_input":
            m 1eka "Oh...{w=0.2} Okay then,{w=0.2} if you say so."
            m 3eua "Just let me know if you change your mind."
            $ mj_playername_skiploopdlg = True
            return
            
        elif mj_playername_attempt == "":
            m 1eksdla ".{w=0.2}.{w=0.2}.{w=0.2}"
            m 3rksdlb "You have to give me a name to call you,{w=0.2} [player]..."
            m 1eua "Try again!"
            $ mj_playername_skiploopdlg = True
            
        elif mj_playername_attempt.lower() == player.lower():
            m 3hub "Okay! I-"
            m 1wud "Wait...{w=0.3}{nw}"
            extend 2etb " Isn't that your current name,{w=0.2} [player]?{nw}"
            $ _history_list.pop()
            menu:
                m  "Wait... isn't that your current name, [player]?{fast}"
                "Yes, I still want to try it.":
                    m 1hua "Ah,{w=0.2} okay!"
                    m 3eub "Let's try it!"
                    
                "You're right, nevermind then.":
                    m 3eka "Well,{w=0.2} try again then!"  
                    $ mj_playername_skiploopdlg = True              

        elif mas_awk_name_comp.search(mj_playername_attempt.lower()):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "Could you pick a more...{w=0.2}{i}appropriate{/i} name please?"
            $ mj_playername_skiploopdlg = True

        elif mas_bad_name_comp.search(mj_playername_attempt.lower()):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Please pick a nicer name for yourself,{w=0.2} okay?"
            $ mj_playername_skiploopdlg = True
            
        elif mas_good_player_name_comp.search(mj_playername_attempt.lower()):
            $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
            m 1sub "[good_quip]"
            m 1hua "Let's try it!"
                    
        ##### all the other reactions, carefully taking from basemods name handling
        else:
            if store.mas_egg_manager.is_eggable_name(mj_playername_attempt.lower()):
                m 1ttu "Are you about this one,{w=0.2} or are you messing with me?{nw}"
                $ _history_list.pop()
                menu:
                    m "Are you about this one, or are you messing with me?{fast}"

                    "Yes, I'm sure.":
                        m 3hub "Well,{w=0.2} let's try it!"
                        #$ persistent._mas_disable_eggs = True'
                        ## todo: add to a sep eggable list so we can sep eggable names when picking names instead of just saving them                        

                    "Maybe...":
                        m 3hub "Well,{w=0.2} let's try it!"
                        #$ persistent._mas_disable_eggs = False         

                
            elif mj_playername_attempt.lower() == "monika" or mj_playername_attempt.lower() == m_name.lower():
                m 1tkc "Really?"
                m 1tku "That's the same as mine!"
                m "Well..."
                m 1eua "Either it really is your name or you're playing a joke on me."
                m 1hua "But it's fine by me if that's what you want me to call you~"
                $ mj_playername_monikareaction = True
                m 3hub "Let's try it!"
                
            else: 
                m 1eub "Okay!{w=0.3}{nw}"
                extend 3eub " Let's try it!"        
                
        if mj_playername_skiploopdlg == False:
            call mj_playername_tryouts
        
            m 3eua "Do you want to try a different name?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want to try a different name?{fast}"
                "Yes":
                    m 1hua "Okay,{w=0.2} [player]!" 
                "No":
                    m 1eka "Alright then,{w=0.2} [player]." 
                    $ done1 = True
        if not done1:
            show monika 1eua
    return

label mj_playername_tryouts:
    ## the actual trying out, but first we need to make some quotes for lack of repeats
    python:  
        mj_random_startquotetime = [
            "Hey [mj_playername_attempt.capitalize()]!",
            "Hello [mj_playername_attempt.capitalize()]~!",
            "Hi [mj_playername_attempt.capitalize()]!{w=0.2} How are you today?",
        ]
        
        mj_random_middlequotetime = [
            "Gosh,{w=0.2} my [bf] [mj_playername_attempt.capitalize()] is the sweetest person I've ever met~",
            "Gosh,{w=0.2} I just want to hug [mj_playername_attempt.capitalize()] all day long~",
            "Gosh,{w=0.2} [mj_playername_attempt.capitalize()] is a really talented individual!{w=0.2} Always helping me out when I need [him]!"
            ]

        mj_random_endquotetime = [
            "I can't wait to see [mj_playername_attempt.capitalize()] face to face one day!",
            "And I hope I get to meet [mj_playername_attempt.capitalize()] in [his] reality one day.",
            "[mj_playername_attempt.capitalize()] is my reason to keep going~!"
        ]
        mj_eggable_namequotetime = [
                "Do you want to go to the festival with me [mj_playername_attempt.capitalize()]~?"
                "Let's walk home together,{w=0.2} [mj_playername_attempt.capitalize()]~",
                ".{w=0.2}.{w=0.2}.{w=0.2}I hope you did your poems last night [mj_playername_attempt.capitalize()]~"
            ] 
            
        mj_randomstart_quip = renpy.substitute(renpy.random.choice(mj_random_startquotetime))
        mj_randommiddle_quip = renpy.substitute(renpy.random.choice(mj_random_middlequotetime))
        mj_randomend_quip = renpy.substitute(renpy.random.choice(mj_random_endquotetime))
        mj_randomegg_quip = renpy.substitute(renpy.random.choice(mj_eggable_namequotetime))
        mj_playername_monikaissorry = False
        mj_quickwordchangeout = "So,"
        
    m 2rtu "Hm.{w=0.2}.{w=0.2}."
    m 3hub"[mj_randomstart_quip]"
    m 2ekbsu"[mj_randommiddle_quip]"
    m 5gkbfa "[mj_randomend_quip]"
    m 5dkbsa "{w=0.2}.{w=0.2}.{w=0.2}."
    
    if mj_playername_monikareaction:
        $ mj_quickchance = renpy.random.random()
        if mj_quickchance < 0.25:
            m 2hsblsdlb "And I swear if [mj_playername_attempt.capitalize()] choose my name just so I'd say nice things about myself-"
            m 2ffblb "You won't hear the end of it!"
            m 2hfu ".{w=0.2}.{w=0.2}.{w=0.2}{nw}"
            extend 1hub "Ahaha!{w=0.2} Kidding!"
            $ mj_quickwordchangeout = "Anyways,"
        
    elif store.mas_egg_manager.is_eggable_name(mj_playername_attempt.lower()):
        extend 3wud " Oh and-{w=0.3}{nw}"
        if mas_safeToRefDokis():
        
            if persistent._mas_pm_cares_about_dokis:
                m 4ttu "[randomegg_quip]"
                m 3hub "Ehehe~!"
            else: 
                $ mj_playername_monikaissorry = True
                if mj_playername_attempt.lower() == "sayori": 
                    m 4ttu "Don't worry [mj_playername_attempt.capitalize()],{w=0.2} I won't leave you {i}hanging{/i}."
                    
                elif mj_playername_attempt.lower() == "yuri":
                    m 4ttu "Don't worry [mj_playername_attempt.capitalize()],{w=0.2} you'll always be a {i}cut{/i} above the rest!"
                    
                elif mj_playername_attempt.lower() == "natsuki":
                    m 4ttu "Don't worry [mj_playername_attempt.capitalize()],{w=0.2} I won't {i}beat{/i} around the bush in any of our conversations."
        else:
            m 4ttu "[randomegg_quip]"
            m 3hub "Ehehe~!"
    
        if mj_playername_monikaissorry:
            m 4huu "..."
            extend 4hksdlb " Sorry,{w=0.2} I couldn't resist with that last one!"
            m 3hub "Ahaha~!"
            $ mj_quickwordchangeout = "Anyways,"
            
    m "[mj_quickwordchangeout]{w=0.3}{nw}"
    extend 1eta " how was that?"
    m 3etb "Do you think '[mj_playername_attempt.capitalize()]' is the one for you?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think '[mj_playername_attempt.capitalize()]' is the one for you?{fast}"
        "Yes I do!":
            m 1hub "Great!"
            if mj_playername_attempt.lower() not in persistent.mj_playername_list:
                m "Do you want me to add it to your list real quick then?{nw}"
                $ _history_list.pop()
                menu:
                    m 1eub "Do you want me to add it to your list real quick then?{fast}"
                    "Yes, and change my name to it!" if mj_playername_attempt.lower() != player.lower():
                        $ persistent.playername = mj_playername_attempt.capitalize()
                        $ player = mj_playername_attempt.capitalize()
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                        m 1hua "You got it [player]!"

                    "Yes!":
                        m 1hua "You got it!"
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                    "No thanks.":
                        m 1eka "Okay then,{w=0.2} [player]."
            else: 
                m 1wud "Oh,{w=0.2}"
                extend 3eub "and it looks like it's already on your list too!"
                extend 1hub " Perfect!"
                m 1hua "Now if you want to use the name,{w=0.2} just let me know!"
            
        "Nah, not really.":
            m 1hksdla "Ah,{w=0.3}{nw}"
            extend 3hsa " that's okay [mas_get_player_nickname()]."
            if mj_playername_monikareaction:
                m 2rksdla "It'd be really confusing for both of us to have the same name anyways."
                m 5eua "So I don't really blame you there,{w=0.3}{nw}"
                extend 5hub " ahaha!"
    return
