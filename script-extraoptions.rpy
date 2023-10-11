## monika picking a name for the player
label mj_playername_pickforplayer:
    #refresh/define these vars/quips rq
    python:
        mj_playername_namepool = []
        mj_playername_randomattempt = ""
        mj_playername_comparisonlist = []
        
        #i went overboard with the list, but at least a big list of names won't have as much repeating quips...
        randomattempt_quips = [
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
        "How does the sound of '[mj_playername_randomattempt.capitalize()]' strike you at all?",
        "My heart says '[mj_playername_randomattempt.capitalize()]'!",
        "My mind says '[mj_playername_randomattempt.capitalize()]'!",
        "My soul says '[mj_playername_randomattempt.capitalize()]'!",
        "What if we took a chance with '[mj_playername_randomattempt.capitalize()]'?"
        ]

    show monika at t11
        
    #quick check if the list is empty/only one option
    if len(persistent.mj_playername_list) == 0:
        m "Well I would, but..."
        m "Your name list is empty [player]."
        m "You need to tell me some names to write down before I can pick one."
        
    #check if the players name is the ONLY name in the list 
    elif len(persistent.mj_playername_list) == 1 and player.lower() in persistent.mj_playername_list:
        m "Well I would, but..."
        m "The only name in your list is your own, [player]."
        m "You need to tell me some more names to write down before I can pick one."
        
    #check if there's only one name in the list that isnt the players 
    elif len(persistent.mj_playername_list) == 1:
        m "Well I would, but..."
        m "There's only one name in the list, [player]."
        m "You need to tell me some more names to write down before I can pick one."
        
    else:
        m "I can do that!"
        m "Do you want me to pick from a certain pool of names or just your whole list?{nw}"
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
        call mj_playername_randomplz
    return

label mj_playername_randomplz:
    m "Let's see..."
    #
    python:
        namepickingloop = True
        namepickingloop2 = False 
        namepicking1sttime = True
        mj_quickrejectednames = []
        
    while namepickingloop:
        m "Hm..."     
        call mj_playername_randomplz_randompick
        $ randomattempt_quip = renpy.substitute(renpy.random.choice(randomattempt_quips))
        m "[randomattempt_quip]{nw}"
        $ _history_list.pop()
        menu: 
            m "[randomattempt_quip]{fast}"
            "Perfect, thanks!":
                ##todo, again checking if the random name is eggable i should maybe do?
                $ persistent.playername = mj_playername_randomattempt.capitalize()
                $ player = mj_playername_randomattempt.capitalize()
                m "Of course [player]!"
                $ namepickingloop = False
                
            "Eh... Try a different one?":
                #add rejected name to list 
                $ mj_quickrejectednames.append(mj_playername_randomattempt)
                call mj_playername_randomplz_randompick
                
            "Nevermind, I'm not really feeling it...":
                m "Ah,"
                extend " that's okay [mas_get_player_nickname()]."
                m "Maybe next time."
                $ namepickingloop = False
    return

# the actual random picking process, it filters out choices the player already rejects during a full round of listing off names so they arent repeated
label mj_playername_randomplz_randompick:
    #random pick the name
        
    $ namepickingloop2 = True
        
    while namepickingloop2:
        $ mj_playername_randomattempt = renpy.substitute(renpy.random.choice(mj_playername_comparisonlist))
        
        #the first time itll do no checks so just quickly end the loop
        if namepicking1sttime:
            $ namepickingloop2 = False
            $ namepicking1sttime = False
        else:
            #after that it needs to check if the name is already rejected or if monika has run out of options
            if set(mj_quickrejectednames) == set(mj_playername_comparisonlist):
                call mj_playername_randomplz_randompickfail
            elif mj_playername_randomattempt in mj_quickrejectednames:
                pass
            else:
                $ namepickingloop2 = False
    return
    
# if the player goes through all availiable names and didnt pick one itll end up here and end the interaction
label mj_playername_randomplz_randompickfail:
    m "Uh... [player]?"
    m "We've gone through all your options and you didn't seem keen on any of them..." 
    m "I... don't think I can be the one to pick a name for you."
    m "Sorry I can't help you more with your indecisiveness on this one but..."
    $ namepickingloop2 = False
    $ namepickingloop = False
    return
    
    
## a menu for when the player just wants to select through some of the names available

label mj_playername_namepoolpick:
    
    #quick check if the list only has 2 options [since theres no point in picking a pool then]
    if len(persistent.mj_playername_list) == 2:
        m "Well, there's not a lot of options to pick from [player]..."
        m "I'll just pick between these two names that are here."
        $ c = persistent.mj_playername_list
    else:
        m "Of course!"
        $ namepoolpicking = True
        while namepoolpicking:
            #make the menu-ready tuple list from the player's names in alphabetical order
            python:
                mj_playername_namepool = []
                mj_playername_tuplelist = []
                persistent.mj_playername_list.sort()
                for mj_playername in persistent.mj_playername_list:
                    mj_playername_tuplelist.append((mj_playername.capitalize(), mj_playername, False, True, False))
        
            #the menu, a checklist
            show monika at t21
            python:
                renpy.say(m, "Select which names you want me to pick from.", interact=False)
                mj_playername_didplayerchoosenames = False
                
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
                
            if len(mj_playername_namepool) == 0:
                m "Hm? Changed your mind [player]?"
                m "Well, let me know if you want to do this later, okay?"
                $ namepoolpicking = False
            elif len(mj_playername_namepool) == 1:           
                m "You need to give me more names than that [player]..."
                m "Try again."
            else:                
                show monika at t11
                m "Okay!"
                $ namepoolpicking = False
    return
    
##deals with enter loop, again, but different for the 'try on a name' option
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
        
        #####reactions to no input/cancel/same name/preexistingname and bad/awk/good names 
        if mj_playername_attempt == "cancel_input":
            m 1eka "Oh... Okay then, if you say so."
            m 3eua "Just let me know if you change your mind."
            $ mj_playername_skiploopdlg = True
            return
            
        elif mj_playername_attempt == "":
            m 1eksdla "..."
            m 3rksdlb "You have to give me a name to call you, [player]..."
            m 1eua "Try again!"
            $ mj_playername_skiploopdlg = True
            
        elif mj_playername_attempt.lower() == player.lower():
            m "Okay! I-"
            m "Wait..."
            extend " isn't that your current name, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m  "Wait... isn't that your current name, [player]?{fast}"
                "Yes, I still want to try it.":
                    m "Ah, okay!"
                    m "Let's try it!"
                    
                "You're right, nevermind.":
                    m "Well, try again then!"  
                    $ mj_playername_skiploopdlg = True              

        ## not needed, make a check at the start in case it's the players name/in the list already and just silently add options if needed
        #elif mj_playername_attempt.lower() in persistent.mj_playername_list:
            #m 1ekd "That name is already on the list, silly!"
            #m 3eka "Try again!"
            #$ mj_playername_skiploopdlg = True
        
        elif mas_awk_name_comp.search(mj_playername_attempt.lower()):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "Could you pick a more...{w=0.2}{i}appropriate{/i} name please?"
            $ mj_playername_skiploopdlg = True

        elif mas_bad_name_comp.search(mj_playername_attempt.lower()):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Please pick a nicer name for yourself, okay?"
            $ mj_playername_skiploopdlg = True
            
        elif mas_good_player_name_comp.search(mj_playername_attempt.lower()):
            $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
            m 1sub "[good_quip]"
            m 1hua "Let's try it!"
                    
        ##### all the other reactions, carefully taking from basemods name handling
        else:
            if store.mas_egg_manager.is_eggable_name(mj_playername_attempt.lower()):
                m 1ttu "Are you about this one, or are you messing with me?{nw}"
                $ _history_list.pop()
                menu:
                    m "Are you about this one, or are you messing with me?{fast}"

                    "Yes, I'm sure.":
                        m "Well, let's try it!"
                        #$ persistent._mas_disable_eggs = True'
                        ## todo: add to a sep eggable list so we can sep eggable names when picking names instead of just saving them                        

                    "Maybe...":
                        m "Well, let's try it!"
                        #$ persistent._mas_disable_eggs = False         

                
            elif mj_playername_attempt.lower() == "monika":
                m 1tkc "Really?"
                m "That's the same as mine!"
                m 1tku "Well..."
                m "Either it really is your name or you're playing a joke on me."
                m 1hua "But it's fine by me if that's what you want me to call you!"
                $ mj_playername_monikareaction = True
                m "Let's try it!"
                
            else: 
                m 1eub "Okay!"
                extend " Let's try it!"        
                
        if mj_playername_skiploopdlg == False:
            call mj_playername_tryouts
        
            m "Do you want to try a different name?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want to try a different name?{fast}"
                "Yes":
                    m 1eua "Okay, [player]!" 
                "No":
                    m 1eua "Alright then, [player]." 
                    $ done1 = True
        if not done1:
            show monika 1eua
    return

label mj_playername_tryouts:
    ## the actual trying out, but first we need to make some quotes for lack of repeats
    python:  
        random_startquotetime = [
            "Hey [mj_playername_attempt.capitalize()]!",
            "Hello [mj_playername_attempt.capitalize()]~!",
            "Hi [mj_playername_attempt.capitalize()]! How are you today?",
        ]
        
        random_middlequotetime = [
            "Gosh, my [bf] [mj_playername_attempt.capitalize()] is the sweetest person I've ever met~",
            "Gosh, I just want to hug [mj_playername_attempt.capitalize()] all day long~",
            "Gosh, [mj_playername_attempt.capitalize()] is a really talented individual! Always helping me out when I need [him]!"
            ]

        random_endquotetime = [
            "I can't wait to see [mj_playername_attempt.capitalize()] face to face one day!",
            "And I hope I get to meet [mj_playername_attempt.capitalize()] in [his] reality one day.",
            "[mj_playername_attempt.capitalize()] is my reason to keep going~!"
        ]
        eggable_namequotetime = [
                "Do you want to go to the festival with me [mj_playername_attempt.capitalize()]~?"
                "Let's walk home together, [mj_playername_attempt.capitalize()]~",
                "...I hope you did your poems last night [mj_playername_attempt.capitalize()]~"
            ] 
            
        randomstart_quip = renpy.substitute(renpy.random.choice(random_startquotetime))
        randommiddle_quip = renpy.substitute(renpy.random.choice(random_middlequotetime))
        randomend_quip = renpy.substitute(renpy.random.choice(random_endquotetime))
        randomegg_quip = renpy.substitute(renpy.random.choice(eggable_namequotetime))
        mj_playername_monikaissorry = False
        
    m "Hm..."
    m "[randomstart_quip]"
    m "[randommiddle_quip]"
    m "[randomend_quip]"
    m "..."
    
    if mj_playername_monikareaction:
        $ quickchance = renpy.random.random()
        if quickchance < 0.25: 
            m "And I swear if [mj_playername_attempt.capitalize()] choosed my name just so I'd say nice things about myself-"
            m "You won't hear the end of it!"
            m "..."
            extend "Ahaha! Kidding!"
        
    if store.mas_egg_manager.is_eggable_name(mj_playername_attempt.lower()):
        extend " Oh and-"
        if mas_safeToRefDokis():
            $ mj_playername_monikaissorry = True

            if mj_playername_attempt.lower() == "sayori": 
                m "Don't worry, I won't leave you {i}hanging{/i} [mj_playername_attempt.capitalize()]."
                
            elif mj_playername_attempt.lower() == "yuri":
                $ eggablenamequotetime.append("You're a {i}cut{/i} above the rest [mj_playername_attempt.capitalize()]!")
                
            elif mj_playername_attempt.lower() == "natsuki":
                $ "Don't worry [mj_playername_attempt.capitalize()], I won't {i}beat{/i} around the bush in any of our conversations."
        else:
            m "[randomegg_quip]"
    
        if mj_playername_monikaissorry:
            m "... Sorry, I couldn't resist with that last one!"
            
    m "Anyways,"
    extend " how was that?"
    m "Do you think '[mj_playername_attempt.capitalize()]' is the one for you?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think '[mj_playername_attempt.capitalize()]' is the one for you?{fast}"
        "Yes I do!":
            m "Great!"
            if mj_playername_attempt.lower not in persistent.mj_playername_list:
                m "Do you want me to add it to your list real quick then?{nw}"
                $ _history_list.pop()
                menu:
                    m "Do you want me to add it to your list real quick then?{fast}"
                    "Yes, and change my name to it!" if mj_playername_attempt.lower() not player.lower():
                        $ persistent.playername = mj_playername_randomattempt.capitalize()
                        $ player = mj_playername_randomattempt.capitalize()
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                        m "You got it [player]!"

                    "Yes!":
                        m "You got it!"
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                    "No thanks.":
                        m "Okay then, [player]."
            else: 
                m "Oh,"
                m "And it looks like it's already on your list too!"
                extend " Perfect!"
                m "Now if you want to use the name, just let me know!"
            
        "Nah, not really.":
            m "Ah,"
            extend " that's okay [mas_get_player_nickname()]."
    return
