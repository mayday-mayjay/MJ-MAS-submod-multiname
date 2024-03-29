##handles the mismatch of the players name
label mj_playername_mismatch:
    if persistent.mj_playermentionedreminder == False:
        m 1esd "Hey [player]?{w=0.2} I noticed you used another dialogue option to change your name."
        m 3rksdla "It can slip my mind to write down new names to your list when you don't use this one..."
        m 3esa "Do you want me to save your current name '[player]' to the list?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want me to save your current name '[player]' to the list?{fast}"
            "Yes please.":
                m 1hub "You got it,{w=0.2} [player]!"
                $ persistent.mj_playername_list.append(player.lower())
                $ persistent.mj_playername_playerdenymismatchentry = False                     
            "No thanks.":
                m 2eka "Okay,{w=0.2} [player]."
                m 1esa "Tell me if you want to add it to the list later though,{w=0.2} okay?"
                $ persistent.mj_playername_playerdenymismatchentry = True
        if persistent.mj_monimentionedreminder < 3:
            m 3hub "You can also tell me if you don't want me to remind you of this anymore."
            $ persistent.mj_monimentionedreminder += 1
            
    else:
        m 1esd "Oh!{w=0.2} [player]!"
        m 3eud "It looks like you're using a name that's not on your list at the moment."
        m 3eub "Do you want me to save your current name '[player]' to the list?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want me to save your current name '[player]' to the list?{fast}"
            "Yes please.":
                m 1hub "You got,{w=0.2} [player]!"
                $ persistent.mj_playername_list.append(player.lower())
                $ persistent.mj_playername_playerdenymismatchentry = False  
            "No thanks.":
                m 2eka "Okay,{w=0.2} [player]."
                m 1esa "Tell me if you want to add it to the list later though,{w=0.2} okay?"
                $ persistent.mj_playername_playerdenymismatchentry = True
    m 1eua "Now then..."
            
    return

    
## deals w the loop of entering the name
    
label mj_playername_enterloop(mj_inputprompt):
    #get players input to compare to reactions, if it passes the reaction it gets added + it doesn't skip loop dlg
    python:
        done1 = False 
        mj_playername_attempt = ""
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
            m 1eka "Oh...{w=0.2} Okay then,{w=0.2} if you say so."
            m 3eua "Just let me know if you change your mind."
            $ mj_playername_skiploopdlg = True
            $ done1 = True
            
        elif mj_playername_attempt == "":
            m 1eksdla ".{w=0.2}.{w=0.2}.{w=0.2}"
            m 3rksdlb "You have to give me a name to call you,{w=0.2} [player]..."
            m 1eua "Try again!"
            $ mj_playername_skiploopdlg = True
            
        elif mj_playername_attempt.lower() in persistent.mj_playername_list:
            m 1ekd "That name is already on the list,{w=0.2} silly!"
            m 3eka "Try again!"
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
            m 3hub "I'll add it to the list right away!"
            m 1hua "Ehehe~"
            $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
            
        elif mj_playername_attempt.lower() == player.lower():
            if persistent.mj_playername_playerdenymismatchentry == True:
                m 3hub "Okay{w=0.2}, I-{w=0.3}{nw}"
                m 1wud "Oh,{w=0.2} hang on!"
                m 2etb "Did you change your mind on adding the new name to the list?{nw}"
                $ _history_list.pop()
                menu:
                    m  "Did you change your mind on adding the new name to the list?{fast}"
                    "Yes, please add it.":
                        m 1hua "You got it!{w=0.3}{nw}"
                        extend 3eub " I'll add it to the list!"
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                        $ persistent.mj_playername_playerdenymismatchentry = False

                    "Actually... No, nevermind.":
                        m 3eka "Well,{w=0.2} try again then!"  
                        $ persistent.mj_playername_playerdenymismatchentry = False
                        $ mj_playername_skiploopdlg = True              
            else:
                m 1eub "Okay then!{w=0.3}{nw}"
                extend 3eub " I'll add it to the list!"
                $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
        
        ##### all the other reactions, carefully taking from basemods name handling
        else:
            if store.mas_egg_manager.is_eggable_name(mj_playername_attempt.lower()):
                m 1ttu "Are you sure this is one of your names,{w=0.2} or are you messing with me?{nw}"
                $ _history_list.pop()
                menu:
                    m "Are you sure this is one of your names, or are you messing with me?{fast}"

                    "Yes, this is one of my names.":
                        m 3hub "Well,{w=0.2} I'll add it to the list then!"
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())

                        #$ persistent._mas_disable_eggs = True'
                        ## todo: add to a sep eggable list so we can sep eggable names when picking names instead of just saving them

                    "Maybe...":
                        m 3hub "Well,{w=0.2} I'll add it to the list anyways,{w=0.2} ahaha!"
                        $ persistent.mj_playername_list.append(mj_playername_attempt.lower())

                        #$ persistent._mas_disable_eggs = False         

                
            elif mj_playername_attempt.lower() == "monika":
                m 1tkc "Really?"
                m 1tku "That's the same as mine!"
                m "Well..."
                m 1eua "Either it really is your name or you're playing a joke on me."
                m 1hua "But it's fine by me if that's what you want me to call you~"
                m 3hub "I'll add it to the list right away!"
                $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
                
            else: 
                m 1eub "Okay then!{w=0.3}{nw}"
                extend 3eub " I'll add it to the list!"
                $ persistent.mj_playername_list.append(mj_playername_attempt.lower())
        
        if mj_playername_skiploopdlg == False:
            m 3eub "Do you want to add another name to the list?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want to add another name to the list?{fast}"
                "Yes":
                    m 1hua "Okay,{w=0.2} [player]!" 
                "No":
                    m 1eka "Alright then,{w=0.2} [player]." 
                    $ done1 = True
        if not done1:
            show monika 1eua
    return


##deals with picking the name
label mj_playername_pick:
    #quick check if the list is empty
    if len(persistent.mj_playername_list) == 0:
        show monika at t11
        m 1rksdla "Your list is empty, [player]{w=0.2}.{w=0.2}.{w=0.2}."
        m 3rksdla "You need to tell me some names to write down before you can pick one."
        m 1hka "So{w=0.2}.{w=0.2}.{w=0.2}."
    #check if the players name is the ONLY name in the list 
    elif len(persistent.mj_playername_list) == 1 and player.lower() in persistent.mj_playername_list:
        show monika at t11
        m 1rksdla "The only name in your list is your own,{w=0.2} [player]."
        m 3rksdla "You need to tell me some more names to write down before you can pick one."
        m 1hka "So{w=0.2}.{w=0.2}.{w=0.2}."
    else:
        #make the menu-ready tuple list from the player's names in alphabetical order
        python:
            mj_playername_tuplelist = []
            persistent.mj_playername_list.sort()
            for mj_playername in persistent.mj_playername_list:
                mj_playername_tuplelist.append((mj_playername.capitalize(), mj_playername, False, False))
            final_args = [("Nevermind", False, False, False, 8)]
    
        #the menu, a genscroll
        show monika at t21
        $ renpy.say(m, "What do you want me to call you?", interact=False)
        call screen mas_gen_scrollable_menu(mj_playername_tuplelist, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_args)
            
        if not _return:  # _return is False
            m 2eka "Okay,{w=0.2} [player]."
    
        else:  # _return has an actual name
            ##todo: add easter egg compatiabilty later 
            $ persistent.playername = _return.capitalize()
            $ player = _return.capitalize()
            m 1eua "Okay!{w=0.3}{nw}"
            extend 3hub " From now on I'll call you [player]!"

    return
    
    
## deals with deleting the names in the list
label mj_playername_deletenames:
    #quick check if the list is empty
    if len(persistent.mj_playername_list) == 0:
        show monika at t11
        m 1rksdla "Your list is empty,{w=0.2} [player]{w=0.2}.{w=0.2}.{w=0.2}."
        m 3rksdla "You need to tell me some names to write down before you can delete them."
        m 1hka "So{w=0.2}.{w=0.2}.{w=0.2}."
                
    else:
        #make the menu-ready tuple list from the player's names in alphabetical order
        python:
            mj_playername_tuplelist = []
            persistent.mj_playername_list.sort()
            for mj_playername in persistent.mj_playername_list:
                mj_playername_tuplelist.append((mj_playername.capitalize(), mj_playername, False, True, False))
    
        #the menu, a checklist
        show monika at t21
        python:
            renpy.say(m, "Select which names you don't want me to call you anymore.", interact=False)
            mj_playername_didplayerdeleteaname= False
            
        call screen mas_check_scrollable_menu( \
            mj_playername_tuplelist, \
            mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, \
            selected_button_prompt=_("Done."), default_button_prompt=_("Done."), \
            return_all=True)
        
        #every item the player selects will be deleted, and a flag will be set for a quick 'done' dlg
        python:
            for mj_playernameitem, mj_playernamedeleteitem in _return.items():
                if mj_playernamedeleteitem is True:
                    persistent.mj_playername_list.remove(mj_playernameitem)
                    mj_playername_didplayerdeleteaname = True
        if mj_playername_didplayerdeleteaname:
            m 1hua "Done!"
    
    return
    

