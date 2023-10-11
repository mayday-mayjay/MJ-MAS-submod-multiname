### there's so many comments here because i'm getting lost in my own code hELP-

default persistent.mj_playername_list = []
default mj_playername_tuplelist = []
default persistent.mj_playername_playerdenymismatchentry = None
default mj_playername_settings_menulist = []
default persistent.mj_playerwantsreminder = True
default persistent.mj_playermentionedreminder = False
default persistent.mj_monimentionedreminder = 0
default mj_playername_menulist = [
    ("Pick a name", "playername_menu_pick", False, False), 
    ("Add a name", "playername_menu_add", False, False), 
    ("Delete a name", "playername_menu_delete", False, False)
]

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multinamemain",
            category=["you"],
            prompt="Test?",
            pool=True,
            unlocked=True,
            #conditional="seen_event('monika_changename')",
            aff_range=(mas_aff.NORMAL, None)
        )
    )
    
##main label that will eventually have be a sep intro topic, quickly grabs players current name at the time to add to the list
label mj_multinamemain:    
    if mas_getEVL_shown_count("mj_multinamemain") < 1:
        #append the players current name to the list 
        python:
            mj_playername_newsess = player.lower()
            persistent.mj_playername_list.append(mj_playername_newsess)
                    
        m "."        
  #after this itd be a sep menu topic that the player asks for  
    else:            
        $ persistent.mj_playername_playerdenymismatchentry = False
        
        #checks for if the player has changed their name with an outside source to something not in the list, does nothing if its already in the list
        if persistent.mj_playerwantsreminder:
            if persistent.playername.lower() not in persistent.mj_playername_list or player.lower() not in persistent.mj_playername_list:                                     
                call mj_playername_mismatch
                    
        call mj_playername_menu
    return 



##the menu, 'nough said
##settings menu for todo; using multiple names in convo? and a 'try on name' option

label mj_playername_menu:
    #start the loop, make the tuples for the menu that change
    python:
        done = False
        mj_namemenu_quip = "What do you want to do?"
        mj_playerusedamenu = False   
    while done is False:
        if mj_playerusedamenu == False:
            $ final_args = [
                ("Can you also...", "playname_menu_settings", True, False, 8),
                ("Nevermind", False, False, False, 0)
            ]
        else: 
            $ final_args = [
                ("Can you also...", "playname_menu_settings", True, False, 8), 
                ("Done", False, False, False, 0)
            ]
        
        # set the menu up, its a genscroll menu
        show monika at t21
        $ renpy.say(m, mj_namemenu_quip, interact=False)
        call screen mas_gen_scrollable_menu(mj_playername_menulist, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_args)

        if not _return:  # _return is False
            show monika at t11
            m 2eka "Okay, [player]."
            extend " Let me know if you need anything!"
            $ done = True
            
        else: #_return has a menu value
            if not mj_playerusedamenu:
                $ mj_playerusedamenu = True
            
            if _return == "playername_menu_add":
                show monika at t11
                m 1eua "Sure!"
                call mj_playername_enterloop("What do you want me to add to the list?")                
            elif _return == "playername_menu_delete":
                m 1eua "Sure!"
                call mj_playername_deletenames                
            elif _return == "playername_menu_pick":
                m 1eua "Sure!"
                call mj_playername_pick
            else:
                call mj_playername_settings

            $ mj_namemenu_quip = "What else do you want to do?"             

    return
        
## quick settings area, only a few options but one day may add more
## todo: can't make a random player var but i can have them ask for moni to pick randomly..? from both the full list + a pool of their choice
## todo: ask her to account for 
label mj_playername_settings:
    $ done2 = False
    
    while done2 is False:
        #make the menu options, one of them switches depending on what the player has previously selected/defaults on
        $ mj_playername_settings_menulist = [
            ("...Pick a name for me?", "playername_menu_pickforplayer", True, False),
            ("...Let me try on a name first?", "playername_menu_trynameplz", True, False)
            ]
        if persistent.mj_playerwantsreminder == True:
            $ mj_playername_settings_menulist.append(("...Not remind me if my name's not on the list.", "playername_menu_noremind", True, False))
        else:
            $ mj_playername_settings_menulist.append(("...Remind me if my name's not on the list.", "playername_menu_remindplz", False, False))
        $ final_args = [("Go back.", False, False, False, 8)]

        #the menu, a genscroll
        show monika at t21
        $ renpy.say(m, mj_namemenu_quip + "{fast}", interact=False)
        call screen mas_gen_scrollable_menu(mj_playername_settings_menulist, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_args)

        if not _return:  # _return is False
            $ mj_namemenu_quip = "What else do you want to do?{fast}"  
            $ done2 = True
            
        else: # _return has a menu valud
            if _return == "playername_menu_pickforplayer":
                call mj_playername_pickforplayer
                                        
            elif _return == "playername_menu_trynameplz":
                show monika at t11
                m "Of course, [mas_get_player_nickname()]."
                call mj_playername_enterloop_tryname("Tell me what name you want to try out!")
            
            elif _return == "playername_menu_remindplz":
                show monika at t11
                m 1eua "Sure!"
                m "I'll be sure to remind you next time you change your name to something not on the list!"
                $ persistent.mj_playerwantsreminder = True
                $ persistent.mj_playermentionedreminder = True
                
            else:
                show monika at t11
                m 1eua "Sure!"
                m "I won't remind you next time you change your name to something not on the list!"
                $ persistent.mj_playerwantsreminder = False
                
        $ mj_namemenu_quip = "What else do you want to do?{fast}"  
    return
            