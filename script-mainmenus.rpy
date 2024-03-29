#vars
default persistent.mj_playername_list = []
default mj_playername_tuplelist = []
default mj_playername_settings_menulist = []

default persistent.mj_playername_playerdenymismatchentry = None
default persistent.mj_playerwantsreminder = True
default persistent.mj_playermentionedreminder = False
default persistent.mj_monimentionedreminder = 0
default persistent.mj_playername_lastnamesubmodacknowledgement = None

default persistent.mj_playername_didsubmodacknowledgement = False
default persistent.mj_playername_reasonfornames = None

default mj_playername_menulist = [
    ("Pick a name", "playername_menu_pick", False, False),
    ("Add a name", "playername_menu_add", False, False),
    ("Delete a name", "playername_menu_delete", False, False)
]

default mj_multiname_reasonmenulist = [
    ("I do it to express my gender.", "gender", False, False),
    ("I have DID/OSDD or I'm part of a system.", "system", False, False),
    ("It's because of my native language/culture.", "culture", False, False),
    ("I go by pennames/nicknames.", "penname", False, False),
    ("I'm trying things out.", "tryout", False, False),
    ("It's mix of different options.", "other", False, False),
    ("Something else...", "other", False, False)
]

### there's so many comments here because i'm getting lost in my own code hELP-
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mj_multiname_main",
            category=["you", "names"],
            prompt="Update [player]'s' name list.",
            pool=True,
            conditional="mas_getEVL_shown_count('mj_multiname_playermultiplenames') > 0",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )
    
label mj_multiname_main:
    $ persistent.mj_playername_playerdenymismatchentry = False

    #checks for if the player has changed their name with an outside source to something not in the list, does nothing if its already in the list
    if persistent.mj_playerwantsreminder:
        if persistent.playername.lower() not in persistent.mj_playername_list or player.lower() not in persistent.mj_playername_list:
            call mj_playername_mismatch

    call mj_playername_mainmenu
return


##the menu, 'nough said
##settings menu for todo; using multiple names in convo?

label mj_playername_mainmenu:
    #start the loop, make the tuples for the menu that change
    python:
        done = False
        mj_namemenu_quip = "What do you want to do?"
        mj_playerusedamenu = False   
    while done is False:
        if mj_playerusedamenu == False:
            $ final_args = [
                ("Can you also...", "playername_menu_settings", True, False, 8),
                ("Nevermind", False, False, False, 0)
            ]
        else: 
            $ final_args = [
                ("Can you also...", "playername_menu_settings", True, False, 8),
                ("Done", False, False, False, 0)
            ]
        
        # set the menu up, its a genscroll menu
        show monika at t21
        $ renpy.say(m, mj_namemenu_quip, interact=False)
        call screen mas_gen_scrollable_menu(mj_playername_menulist, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_args)

        if not _return:  # _return is False
            show monika at t11
            m 2eka "Okay,{w=0.2} [player]."
            extend 3hua " Let me know if you need anything!"
            $ done = True
            
        else: #_return has a menu value
            if not mj_playerusedamenu:
                $ mj_playerusedamenu = True
            
            if _return == "playername_menu_add":
                show monika at t11
                m 1hua "Sure!"
                call mj_playername_enterloop("What do you want me to add to the list?")                
            elif _return == "playername_menu_delete":
                m 1hua "Sure!"
                call mj_playername_deletenames                
            elif _return == "playername_menu_pick":
                m 1hua "Sure!"
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
        python:
             mj_playername_settings_menulist = [
                ("...Pick a name for me?", "playername_menu_pickforplayer", True, False),
                ("...Let me try on a name?", "playername_menu_trynameplz", True, False)
            ]

        if persistent.mj_playerwantsreminder:
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
                m 1eub "Of course, [mas_get_player_nickname()]."
                call mj_playername_enterloop_tryname("Tell me what name you want to try out!")
            
            elif _return == "playername_menu_remindplz":
                show monika at t11
                m 1hub"Sure!"
                m 3eua "I'll be sure to remind you the next time you change your name to something not on the list!"
                $ persistent.mj_playerwantsreminder = True
                $ persistent.mj_playermentionedreminder = True
                
            else:
                show monika at t11
                m 1hub "Sure!"
                m 3eua "I won't remind you the next time you change your name to something not on the list!"
                $ persistent.mj_playerwantsreminder = False
                
        $ mj_namemenu_quip = "What else do you want to do?{fast}"  
    return "prompt"
            