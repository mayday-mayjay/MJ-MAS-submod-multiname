#saves players current name into a seperate variable for main and 'old' for later use
default persistent._mj_saveplayer_mainname = None
default persistent._mj_saveplayer_oldname = None



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="submod_varitest",
            category=["you"],
            prompt="Test?",
            pool=True,
            unlocked=True,
            rules={"bookmark_rule": mas_bookmarks_derand.WHITELIST},
            #conditional="seen_event('monika_changename')",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label submod_varitest:
#grabbing ev shown counts for main part
    $ ev = mas_getEV("submod_varitest")

    
    if ev.shown_count == 0:

        python:
            submod_playernamelist = []
            submod_playernamelist.append((player.capitalize(), player.capitalize(), False, False))
        
        #grabs base mods change name ev/seen for later use
            grabnametopic = mas_getEV("monika_changename")
            persistent.submod_changednameusingbase_1 = grabnametopic.shown_count

        python:
            persistent._mj_saveplayer_mainname = player
            persistent._mj_saveplayer_oldname = player

        #filler dialogue to see vars work, save old name after first time use with this
        m 1eua "Hi! [player]! Or is it [persistent._mj_saveplayer_mainname]? Or maybe [persistent._mj_saveplayer_oldname]? Either way I hope your having a nice day!"


    elif ev.shown_count > 0:
        $ persistent.submod_changednameusingbase_2 = mas_getEV("monika_changename")
        python:
            persistent._mj_saveplayer_mainname = player

        #checks for if the player interacted with the 'i changed my name' event and if the name was actually changed with it
        if persistent.submod_changednameusingbase_2.shown_count > persistent.submod_changednameusingbase_1:

            if persistent._mj_saveplayer_oldname == persistent._mj_saveplayer_mainname:
                
                #refresh change topic count, jump straight to name change as if nothing happened
                $ grabnametopic = mas_getEV("monika_changename")
                $ persistent.submod_changednameusingbase_1 = grabnametopic.shown_count
                jump name_change_temp


            else:
                #regrabs the ev to refresh it
                $ grabnametopic = mas_getEV("monika_changename")
                $ persistent.submod_changednameusingbase_1 = grabnametopic.shown_count

                jump mj_playername_mismatch


        else: 
            jump name_change_temp


label name_change_temp:
m 1eua "What do you want to do?"
$ _history_list.pop()
menu:
    m "What do you want to do?{fast}"

    "Add a name":
        call submod_player_enter_addname_loop("What do you want me to add to the list?")
        jump name_change_temp
    "Delete a name":
        m 1eua "Sure!"
        jump placeholder_area
    "Pick a name":
        m 1eua "Sure!"
        jump placeholder_area
    "Nevermind":
        jump mj_playerdone



label submod_player_enter_addname_loop(input_prompt):
    python:
        done = False 
        name_addattempt = ""

    while not done:
        python:
            submod_tempname = mas_input(
                "[input_prompt]",
                length=20,
                screen_kwargs={"use_return_button": True}
            ).strip(' \t\n\r')

            name_addattempt = submod_tempname.lower()

        if name_addattempt == "cancel_input":
            m 1eka "Oh... Okay then, if you say so."
            m 3eua "Just let me know if you change your mind."
            $ done = True

        elif name_addattempt == "":
            m 1eksdla "..."
            m 3rksdlb "You have to give me a name to call you, [player]..."
            m 1eua "Try again!"

        elif name_addattempt == player.lower():
            m 2hua "..."
            m 4hksdlb "That's the same name you have right now, silly!"
            m 1eua "Try again~"

        elif mas_awk_name_comp.search(submod_tempname):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "Could you pick a more...{w=0.2}{i}appropriate{/i} name please?"

        elif mas_bad_name_comp.search(submod_tempname):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Please pick a nicer name for yourself, okay?"
        
        #elif submod_playernamelist.search(submod_tempname):
            #m 1ekd "That name is already on the list, silly!"
            #m 3eka "Try again~"

        else:
            # easter egg name checks
            if store.mas_egg_manager.is_eggable_name(name_addattempt):
                m 1ttu "Are you sure this is your real name, or are you messing with me?{nw}"
                $ _history_list.pop()
                menu:
                    m "Are you sure this is your real name, or are you messing with me?{fast}"

                    "Yes, this is my name":
                        $ persistent._mas_disable_eggs = True

                    "Maybe...":
                        $ persistent._mas_disable_eggs = False
            #this area is not needed because the name change isn't here, will reimplement when using pick a name

            #python:
                #old_name = persistent.playername.lower()
                #done = True

                # adjust names
                #persistent.mcname = player
                #mcname = player
                #persistent.playername = submod_tempname
                #player = submod_tempname

            # egg adjustments
            # MUST BE AFTER THE NAME ADJUSTMENT
            #if store.mas_egg_manager.sayori_enabled():
                #call sayori_name_scare

            #elif old_name == "sayori":
                # reset music choices
                #$ songs.initMusicChoices()

            # name reactions
            if name_addattempt == "monika":
                m 1tkc "Really?"
                m "That's the same as mine!"
                m 1tku "Well..."
                m "Either it really is your name or you're playing a joke on me."
                m 1hua "But it's fine by me if that's what you want me to call you~"
                m 1hua "I'll add it to the list right away~!"
                $ submod_playernamelist.append((name_addattempt.capitalize(), name_addattempt.capitalize(), False, False))

            elif mas_good_player_name_comp.search(submod_tempname):
                $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
                m 1sub "[good_quip]"
                m 3esa "Okay then! I'll add it to the list!"
                $ submod_playernamelist.append((name_addattempt.capitalize(), name_addattempt.capitalize(), False, False))
                m 1hua "Ehehe~"

            else:
                m 1eub "Okay then!"
                $ submod_playernamelist.append((name_addattempt.capitalize(), name_addattempt.capitalize(), False, False))
                m 3eub "I'll add it to the list!"
        
        menu:
            m "Do you want to add another name to the list?{fast}"

            "Yes":
                m 1eua "Okay, [player]!" 
            "No":
                m 1eua "Alright then, [player]." 
                $ done = True
        if not done:
            show monika 1eua

    return

label placeholder_area:
menu:
    "You haven't made this section yet, silly! ~Chibika":
        m 1esc "Did... you just pick a dialogue option?"
        m 1esc "I don't remember starting a conversation... What did that option do...?"
menu:
    "It's just some testing, don't worry about it darling":
        m 1esc "Well, if you say so."
        m 1hua "Let's just carry on with the day, okay?"
        jump mj_playerdone



label mj_playername_mismatch:
m 1eua "Hey [player]? I noticed you used another dialouge option to change your name."
m 1eua "It sorta slips my mind to write down new names to the list when you don't use this..."
m 1eua "But I did make sure to take note of a previous name you had before this one, so I could bring it up!"
m 1eua "Do you want me to save your old name '[persistent._mj_saveplayer_oldname]' to the list?"
$ _history_list.pop()
menu:
    m "Want me to save your old name to the list?{fast}"

    "Yes please.":
        m 1eua "Okay, [player]!"
        jump name_change_temp
        # future plans, compare list for dupes and/or add it to the list
    "No thanks.":
        m 1eua "Okay, [player]."
        m 1eua "Tell me if you want to add [persistent._mj_saveplayer_oldname] to the list later though, okay?"
        
        #old name gets discarded and replaced with main name in case player does it again
        python:
            persistent._mj_saveplayer_oldname = persistent._mj_saveplayer_mainname
        jump name_change_temp



label mj_playerdone:
return