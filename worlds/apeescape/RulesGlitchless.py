from .Regions import connect_regions, ApeEscapeLevel
from .Strings import AEItem, AERoom

# TODO: Add the key locking logic on a level by level basis. Don't forget the other two Rules files!
# TODO: Reference the levellist to determine how many keys each level needs
# Changelog: Replaced "AEWorld.Wn.value" with "Menu"
# Added hardcoded key logic to the Jake races (needs replacing with correct values!)
def set_glitchless_rules(self):
    # This is the logic for being able to catch every monkey to access the second Specter fight. The logic for the fight itself would be Sling + CanHitMultiple + Net.
    # Make sure to update this condition properly when alternate Peak Point Matrix unlock conditions are added.
    if self.options.goal == "second":
        connect_regions(self, "Menu", AERoom.W9L2Boss.value,
                        lambda state: Keys(state, self, self.levellist[21].keys) and HasNet(state, self) and HasSling(state, self) and HasHoop(state, self) and HasFlyer(state, self) and CanHitMultiple(state, self) and HasRC(state, self))

    #Time Station
    connect_regions(self, "Menu", AERoom.TimeStationMain.value, lambda state: True)
    connect_regions(self, "Menu", AERoom.TimeStationMinigame.value, lambda state: True)
    connect_regions(self, "Menu", AERoom.TimeStationTraining.value, lambda state: True)

    # 1-1
    connect_regions(self, "Menu", AERoom.W1L1Main.value, lambda state: self.levellist[0].keys)

    connect_regions(self, AERoom.W1L1Main.value, AERoom.W1L1Noonan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AERoom.W1L1Jorjy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AERoom.W1L1Nati.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AERoom.W1L1TrayC.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))

    # 1-2
    connect_regions(self, "Menu", AERoom.W1L2Main.value, lambda state: True)

    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2Shay.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2DrMonk.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2Ahchoo.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2Grunt.value,
                    lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2Tyrone.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AERoom.W1L2Gornif.value,
                    lambda state: CanSwim(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))

    # 1-3
    connect_regions(self, "Menu", AERoom.W1L3Entry.value, lambda state: True)
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Volcano.value, lambda state: True)
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Triceratops.value, lambda state: True)

    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Scotty.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Coco.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3JThomas.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Moggan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Volcano.value, AERoom.W1L3Barney.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Volcano.value, AERoom.W1L3Mattie.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Triceratops.value, AERoom.W1L3Rocky.value,
                    lambda state: HasSling(state, self) and CanHitMultiple(state, self) and HasNet(state, self))

    # 2-1
    connect_regions(self, "Menu", AERoom.W2L1Entry.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Mushroom.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Fish.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Fish.value, AERoom.W2L1Tent.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Tent.value, AERoom.W2L1Boulder.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Boulder.value, lambda state: True)

    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Marquez.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Livinston.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1George.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.W2L1Gonzo.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.W2L1Zanzibar.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.W2L1Alphonse.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AERoom.W2L1Maki.value,
                    lambda state: TJ_FishEntry(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AERoom.W2L1Herb.value,
                    lambda state: TJ_FishEntry(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AERoom.W2L1Dilweed.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AERoom.W2L1Stoddy.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AERoom.W2L1Mitong.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AERoom.W2L1Nasus.value,
                    lambda state: (TJ_FishEntry(state, self) or (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Boulder.value, AERoom.W2L1Elehcim.value,
                    lambda state: (TJ_UFOEntry(state, self) or (TJ_FishEntry(state, self) and CanHitMultiple(state, self))) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Boulder.value, AERoom.W2L1Selur.value,
                    lambda state: ((TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self)) or (TJ_FishEntry(state, self) and CanHitMultiple(state, self))) and HasSling(state, self) and HasNet(state, self))

    # 2-2
    connect_regions(self, "Menu", AERoom.W2L2Outside.value, lambda state: True)
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Fan.value, lambda state: True)
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Obelisk.value, lambda state: True)
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Water.value, lambda state: True)

    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Kyle.value,
                    lambda state: (CanHitOnce(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Stan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Kenny.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Cratman.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Mooshy.value,
                    lambda state: HasHoop(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Fan.value, AERoom.W2L2Nuzzy.value,
                    lambda state: (HasSling(state, self) or HasHoop(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Fan.value, AERoom.W2L2Mav.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AERoom.W2L2Papou.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AERoom.W2L2Trance.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AERoom.W2L2Bernt.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AERoom.W2L2Runt.value,
                    lambda state: CanSwim(state, self) and (HasSling(state, self) or HasHoop(state, self)) and (CanHitOnce(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AERoom.W2L2Hoolah.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AERoom.W2L2Chino.value,
                    lambda state: CanSwim(state, self) and (HasSling(state, self) or HasHoop(state, self)) and (CanHitOnce(state, self) or HasFlyer(state, self)) and HasNet(state, self))

    # 2-3
    connect_regions(self, "Menu", AERoom.W2L3Outside.value, lambda state: True)
    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Side.value, lambda state: True)
    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Main.value, lambda state: True)
    connect_regions(self, AERoom.W2L3Main.value, AERoom.W2L3Pillar.value, lambda state: True)

    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Bazzle.value,
                    lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Freeto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L3Side.value, AERoom.W2L3Troopa.value,
                    lambda state: (HasSling(state, self) or (HasFlyer(state, self) and CanHitOnce(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Main.value, AERoom.W2L3Stymie.value,
                    lambda state: CR_Inside(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Main.value, AERoom.W2L3Spanky.value,
                    lambda state: CR_Inside(state, self) and CanSwim(state, self) and (HasMobility(state, self) or CanHitMultiple(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Main.value, AERoom.W2L3Jesta.value,
                    lambda state: CR_Inside(state, self) and (CanHitMultiple(state, self) or (CanSwim(state, self) and HasMobility(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Pillar.value, AERoom.W2L3Pally.value,
                    lambda state: CR_Inside(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Pillar.value, AERoom.W2L3Crash.value,
                    lambda state: CR_Inside(state, self) and RCMonkey(state, self) and HasNet(state, self))

    # 4-1
    connect_regions(self, "Menu", AERoom.W4L1FirstRoom.value, lambda state: True)
    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1SecondRoom.value, lambda state: True)

    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1CoolBlue.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1Sandy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1ShellE.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1Gidget.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.W4L1Shaka.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.W4L1Puka.value,
                    lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.W4L1MaxMahalo.value,
                    lambda state: HasSling(state, self) and HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.W4L1Moko.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))

    # 4-2
    connect_regions(self, "Menu", AERoom.W4L2FirstRoom.value, lambda state: True)
    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2SecondRoom.value, lambda state: True)

    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2Chip.value,
                    lambda state: CanSwim(state, self) and CanWaterCatch(state, self))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2Oreo.value,
                    lambda state: ((HasHoop(state, self) and CanHitMultiple(state, self) and CanSwim(state, self)) or HasMobility(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2Puddles.value,
                    lambda state: CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2Kalama.value,
                    lambda state: ((HasHoop(state, self) and CanHitMultiple(state, self) and CanSwim(state, self)) or HasMobility(state, self)) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.W4L2Iz.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.W4L2BongBong.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.W4L2Jux.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.W4L2Pickles.value,
                    lambda state: CanSwim(state, self) and CanHitMultiple(state, self) and HasNet(state, self))

    # 4-3
    connect_regions(self, "Menu", AERoom.W4L3Outside.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Outside.value, AERoom.W4L3Stomach.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Stomach.value, AERoom.W4L3Slide.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Slide.value, AERoom.W4L3Gallery.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Tentacle.value, lambda state: True)

    connect_regions(self, AERoom.W4L3Outside.value, AERoom.W4L3TonTon.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Outside.value, AERoom.W4L3Stuw.value,
                    lambda state: (CanSwim(state, self) or CanHitOnce(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Stomach.value, AERoom.W4L3Mars.value,
                    lambda state: CanHitOnce(state, self) and HasRC(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W4L3Stomach.value, AERoom.W4L3Murky.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Stomach.value, AERoom.W4L3Horke.value,
                    lambda state: (CanHitOnce(state, self) and (CanSwim(state, self) or HasFlyer(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Howeerd.value,
                    lambda state: DI_SecondHalf(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Robbin.value,
                    lambda state: DI_SecondHalf(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Jakkee.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Frederic.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Baba.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Tentacle.value, AERoom.W4L3Quirck.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))

    # 5-1
    connect_regions(self, "Menu", AERoom.W5L1Main.value, lambda state: True)

    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Popcicle.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Iced.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Rickets.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Skeens.value,
                    lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Chilly.value,
                    lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AERoom.W5L1Denggoy.value,
                    lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))

    # 5-2
    connect_regions(self, "Menu", AERoom.W5L2Entry.value, lambda state: True)
    connect_regions(self, AERoom.W5L2Caverns.value, AERoom.W5L2Water.value, lambda state: True)
    connect_regions(self, AERoom.W5L2Entry.value, AERoom.W5L2Caverns.value, lambda state: True)

    connect_regions(self, AERoom.W5L2Entry.value, AERoom.W5L2Storm.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Entry.value, AERoom.W5L2Qube.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AERoom.W5L2Ranix.value,
                    lambda state: HasFlyer(state, self) and HasSling(state, self) and (HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self))))
    connect_regions(self, AERoom.W5L2Water.value, AERoom.W5L2Sharpe.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AERoom.W5L2Sticky.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AERoom.W5L2Droog.value,
                    lambda state: HasFlyer(state, self) and CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Caverns.value, AERoom.W5L2Gash.value,
                    lambda state: HasFlyer(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W5L2Caverns.value, AERoom.W5L2Kundra.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Caverns.value, AERoom.W5L2Shadow.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))

    # 5-3
    connect_regions(self, "Menu", AERoom.W5L3Outside.value, lambda state: True)
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Spring.value, lambda state: True)
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Cave.value, lambda state: True)

    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Punky.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Ameego.value,
                    lambda state: CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Yoky.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Jory.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AERoom.W5L3Crank.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AERoom.W5L3Claxter.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AERoom.W5L3Looza.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Cave.value, AERoom.W5L3Roti.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Cave.value, AERoom.W5L3Dissa.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))

    # 7-1
    connect_regions(self, "Menu", AERoom.W7L1Outside.value, lambda state: True)
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Temple.value, lambda state: True)
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Well.value, lambda state: True)

    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Taku.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Rocka.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Maralea.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Wog.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AERoom.W7L1Mayi.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AERoom.W7L1Owyang.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AERoom.W7L1Long.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AERoom.W7L1Elly.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AERoom.W7L1Chunky.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Well.value, AERoom.W7L1Voti.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Well.value, AERoom.W7L1QuelTin.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Well.value, AERoom.W7L1Phaldo.value,
                    lambda state: HasNet(state, self))

    # 7-2
    connect_regions(self, "Menu", AERoom.W7L2First.value, lambda state: True)
    connect_regions(self, AERoom.W7L2First.value, AERoom.W7L2Gong.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Gong.value, AERoom.W7L2Middle.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Middle.value, AERoom.W7L2Course.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Course.value, AERoom.W7L2Barrel.value, lambda state: True)

    connect_regions(self, AERoom.W7L2First.value, AERoom.W7L2Minky.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2First.value, AERoom.W7L2Zobbro.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AERoom.W7L2Xeeto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AERoom.W7L2Moops.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AERoom.W7L2Zanabi.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Middle.value, AERoom.W7L2Doxs.value,
                    lambda state: WSW_ThirdRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Course.value, AERoom.W7L2Buddha.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Course.value, AERoom.W7L2Fooey.value,
                    lambda state: WSW_ThirdRoom(state, self) and RCMonkey(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Barrel.value, AERoom.W7L2Kong.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Barrel.value, AERoom.W7L2Phool.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))

    # 7-3
    connect_regions(self, "Menu", AERoom.W7L3Outside.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Castle.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Bell.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Elevator.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Elevator.value, AERoom.W7L3Basement.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Basement.value, AERoom.W7L3Button.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Boss.value,
                    lambda state: CanHitMultiple(state, self) and CC_ButtonRoom(state, self))

    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Robart.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Igor.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Naners.value,
                    lambda state: HasNet(state, self))
    # CC_5Monkeys access rule specifically checks for the ability to catch 5 monkeys, so Net is already part of that check.
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Neeners.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Charles.value,
                    lambda state: HasPunch(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Gustav.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Wilhelm.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Emmanuel.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3SirCutty.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AERoom.W7L3Calligan.value,
                    lambda state: CC_WaterRoom(state, self) and (CanDive(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AERoom.W7L3Castalist.value,
                    lambda state: CC_WaterRoom(state, self) and CanDive(state, self) and CanWaterCatch(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AERoom.W7L3Deveneom.value,
                    lambda state: CC_ButtonRoom(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W7L3Button.value, AERoom.W7L3Astur.value,
                    lambda state: CC_ButtonRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Button.value, AERoom.W7L3Kilserack.value,
                    lambda state: CC_ButtonRoom(state, self) and (HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self))))
    connect_regions(self, AERoom.W7L3Elevator.value, AERoom.W7L3Ringo.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Elevator.value, AERoom.W7L3Densil.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Elevator.value, AERoom.W7L3Figero.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AERoom.W7L3Fej.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AERoom.W7L3Joey.value,
                    lambda state: HasMobility(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AERoom.W7L3Donqui.value,
                    lambda state: HasNet(state, self))

    # 8-1
    connect_regions(self, "Menu", AERoom.W8L1Outside.value, lambda state: True)
    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Sewers.value, lambda state: True)
    connect_regions(self, AERoom.W8L1Sewers.value, AERoom.W8L1Barrel.value, lambda state: True)

    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Kaine.value,
                    lambda state: RCMonkey(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Jaxx.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Gehry.value,
                    lambda state: CP_FrontBarrels(state, self) and CanDive(state, self) and HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Alcatraz.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AERoom.W8L1Tino.value,
                    lambda state: CP_FrontSewer(state, self) and HasRC(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AERoom.W8L1QBee.value,
                    lambda state: CP_FrontSewer(state, self) and HasRC(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AERoom.W8L1McManic.value,
                    lambda state: CP_FrontSewer(state, self) and HasRC(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1Dywan.value,
                    lambda state: CP_FrontBarrels(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1CKHutch.value,
                    lambda state: CP_FrontBarrels(state, self) and HasFlyer(state, self) and CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1Winky.value,
                    lambda state: CP_FrontBarrels(state, self) and HasFlyer(state, self) and (HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self))))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1BLuv.value,
                    lambda state: CP_FrontBarrels(state, self) and HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1Camper.value,
                    lambda state: CP_FrontBarrels(state, self) and CanDive(state, self) and HasFlyer(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W8L1Barrel.value, AERoom.W8L1Huener.value,
                    lambda state: CP_FrontBarrels(state, self) and CanSwim(state, self) and HasFlyer(state, self) and HasNet(state, self))

    # 8-2
    connect_regions(self, "Menu", AERoom.W8L2Outside.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Outside.value, AERoom.W8L2Factory.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2RC.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2Wheel.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2Mech.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Mech.value, AERoom.W8L2Lava.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Lava.value, AERoom.W8L2Conveyor.value, lambda state: True)

    connect_regions(self, AERoom.W8L2Outside.value, AERoom.W8L2BigShow.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L2Outside.value, AERoom.W8L2Dreos.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2Reznor.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2RC.value, AERoom.W8L2Urkel.value,
                    lambda state: SF_CarRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AERoom.W8L2VanillaS.value,
                    lambda state: SF_MechRoom(state, self) and HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AERoom.W8L2Radd.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AERoom.W8L2Shimbo.value,
                    lambda state: SF_MechRoom(state, self) and RCMonkey(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Conveyor.value, AERoom.W8L2Hurt.value,
                    lambda state: SF_MechRoom(state, self) and CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Conveyor.value, AERoom.W8L2String.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Mech.value, AERoom.W8L2Khamo.value,
                    lambda state: SF_MechRoom(state, self) and CanHitMultiple(state, self) and HasNet(state, self))

    # 8-3
    connect_regions(self, "Menu", AERoom.W8L3Outside.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Outside.value, AERoom.W8L3Lobby.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Water.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Tank.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Fan.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Boss.value,
                    lambda state: TVT_TankRoom(state, self) and HasSling(state, self))

    connect_regions(self, AERoom.W8L3Outside.value, AERoom.W8L3Fredo.value,
                    lambda state: HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Water.value, AERoom.W8L3Charlee.value,
                    lambda state: TVT_HitButton(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Water.value, AERoom.W8L3Mach3.value,
                    lambda state: TVT_HitButton(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Tortuss.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Manic.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Ruptdis.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Eighty7.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Danio.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AERoom.W8L3Roosta.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AERoom.W8L3Tellis.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AERoom.W8L3Whack.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AERoom.W8L3Frostee.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))

    # 9-1
    connect_regions(self, "Menu", AERoom.W9L1Hub.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Hub.value, AERoom.W9L1Entry.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1Coaster1.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Coaster1.value, AERoom.W9L1Coaster2.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Coaster2.value, AERoom.W9L1Haunted.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Haunted.value, AERoom.W9L1Coffin.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Coffin.value, AERoom.W9L1Natalie.value, lambda state: MM_Natalie(state, self))
    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1Circus.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Circus.value, AERoom.W9L1Professor.value, lambda state: MM_Professor(state, self))
    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1GoKarz.value, lambda state: True)
    connect_regions(self, AERoom.W9L1GoKarz.value, AERoom.W9L1Jake.value, lambda state: MM_Jake(state, self))
    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1Western.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1Crater.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Crater.value, AERoom.W9L1Outside.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Outside.value, AERoom.W9L1Side.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Outside.value, AERoom.W9L1Castle.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Head.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Climb1.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Climb1.value, AERoom.W9L1Climb2.value, lambda state: True)
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Boss.value, lambda state: MM_FinalBoss(state, self))

    connect_regions(self, AERoom.W9L1Entry.value, AERoom.W9L1Goopo.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Haunted.value, AERoom.W9L1Porto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AERoom.W9L1Slam.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AERoom.W9L1Junk.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AERoom.W9L1Crib.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AERoom.W9L1Nak.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AERoom.W9L1Cloy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AERoom.W9L1Shaw.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AERoom.W9L1Flea.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Crater.value, AERoom.W9L1Schafette.value,
                    lambda state: MM_SHA(state, self) and HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Outside.value, AERoom.W9L1Donovan.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Outside.value, AERoom.W9L1Laura.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Uribe.value,
                    lambda state: MM_UFODoor(state, self) and HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Gordo.value,
                    lambda state: MM_UFODoor(state, self) and HasRC(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Raeski.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AERoom.W9L1Poopie.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb1.value, AERoom.W9L1Teacup.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb1.value, AERoom.W9L1Shine.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb2.value, AERoom.W9L1Wrench.value,
                    lambda state: MM_SpaceMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb2.value, AERoom.W9L1Bronson.value,
                    lambda state: MM_SpaceMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AERoom.W9L1Bungee.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AERoom.W9L1Carro.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AERoom.W9L1Carlito.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Side.value, AERoom.W9L1BG.value,
                    lambda state: MM_SHA(state, self) and HasSling(state, self) and HasNet(state, self))

    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player, 1)


    if self.options.coin == "true":
        # Coins
        # 1-1
        connect_regions(self, AERoom.W1L1Main.value, AERoom.Coin1.value,
                        lambda state: NoRequirement())
        # 1-2
        connect_regions(self, AERoom.W1L2Main.value, AERoom.Coin2.value,
                        lambda state: CanDive(state, self))
        # 1-3
        connect_regions(self, AERoom.W1L3Entry.value, AERoom.Coin3.value,
                        lambda state: NoRequirement())
        # 2-1
        connect_regions(self, AERoom.W2L1Entry.value, AERoom.Coin6.value,
                        lambda state: HasMobility(state, self))
        connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.Coin7.value,
                        lambda state: TJ_Mushroom(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AERoom.Coin8.value,
                        lambda state: (TJ_FishEntry(state, self)))
        connect_regions(self, AERoom.W2L1Tent.value, AERoom.Coin9.value,
                        lambda state: (TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or ((TJ_UFOEntry(state, self)) and (TJ_UFOCliff(state, self))))
        # 2-2
        connect_regions(self, AERoom.W2L2Outside.value, AERoom.Coin11.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AERoom.Coin12.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Obelisk.value, AERoom.Coin13.value,
                        lambda state: HasRC(state, self) or HasPunch(state, self))
        connect_regions(self, AERoom.W2L2Water.value, AERoom.Coin14.value,
                        lambda state: (CanDive(state, self)) and ((CanHitOnce(state, self)) or (HasFlyer(state, self))))
        # 2-3
        connect_regions(self, AERoom.W2L3Main.value, AERoom.Coin17.value,
                        lambda state: (CR_Inside(state, self)) and ((CanHitMultiple(state, self)) and (CanSwim(state, self))) or (HasMobility(state, self)))
        # 3-1
        connect_regions(self, "Menu", AERoom.Coin19.value,
                        lambda state: CanSwim(state, self) and Keys(state, self, self.levellist[6].keys))
        # 4-1
        connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.Coin21.value,
                        lambda state: HasNet(state, self))
        # 4-2
        connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.Coin23.value,
                        lambda state: CanDive(state, self))
        # 4-3
        connect_regions(self, AERoom.W4L3Outside.value, AERoom.Coin24.value,
                        lambda state: CanSwim(state, self) or CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Stomach.value, AERoom.Coin25.value,
                        lambda state: CanDive(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Slide.value, AERoom.Coin28.value,
                        lambda state: (CanSwim(state, self) and ((CanHitOnce(state, self) and HasNet(state, self)) or HasPunch(state, self))))
        # 5-1
        connect_regions(self, AERoom.W5L1Main.value, AERoom.Coin29.value,
                        lambda state: NoRequirement())
        # 5-2
        connect_regions(self, AERoom.W5L2Entry.value, AERoom.Coin30.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W5L2Water.value, AERoom.Coin31.value,
                        lambda state: HasFlyer(state, self) and CanDive(state, self))
        connect_regions(self, AERoom.W5L2Caverns.value, AERoom.Coin32.value,
                        lambda state: HasFlyer(state, self))
        # 5-3
        connect_regions(self, AERoom.W5L3Spring.value, AERoom.Coin34.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W5L3Cave.value, AERoom.Coin35.value,
                        lambda state: CanHitMultiple(state, self))
        # 6-1
        connect_regions(self, "Menu", AERoom.Coin36.value,
                        lambda state: HasFlyer(state, self) and Keys(state, self, self.levellist[13].keys))
        # 7-1
        connect_regions(self, AERoom.W7L1Outside.value, AERoom.Coin37.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L1Temple.value, AERoom.Coin38.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L1Well.value, AERoom.Coin39.value,
                        lambda state: HasFlyer(state, self))
        # 7-2
        connect_regions(self, AERoom.W7L2First.value, AERoom.Coin40.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L2Gong.value, AERoom.Coin41.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L2Barrel.value, AERoom.Coin44.value,
                        lambda state: HasFlyer(state, self))
        # 7-3
        connect_regions(self, AERoom.W7L3Outside.value, AERoom.Coin45.value,
                        lambda state: HasClub(state, self) or HasFlyer(state, self) or HasPunch(state, self))
        connect_regions(self, AERoom.W7L3Castle.value, AERoom.Coin46.value,
                        lambda state: CC_5Monkeys(state, self))
        connect_regions(self, AERoom.W7L3Button.value, AERoom.Coin49.value,
                        lambda state: CC_ButtonRoom(state, self))
        connect_regions(self, AERoom.W7L3Elevator.value, AERoom.Coin50.value,
                        lambda state: CC_5Monkeys(state, self) or CC_WaterRoom(state, self))
        # 8-1
        connect_regions(self, AERoom.W8L1Outside.value, AERoom.Coin53.value,
                        lambda state: CP_FrontBarrels(state, self) and CanDive(state, self) and HasFlyer(state, self))
        connect_regions(self, AERoom.W8L1Sewers.value, AERoom.Coin54.value,
                        lambda state: CP_FrontSewer(state, self) and HasRC(state, self))
        connect_regions(self, AERoom.W8L1Barrel.value, AERoom.Coin55.value,
                        lambda state: CP_FrontBarrels(state, self) and HasFlyer(state, self))
        # 8-2
        connect_regions(self, AERoom.W8L2RC.value, AERoom.Coin58.value,
                        lambda state: SF_CarRoom(state, self))
        connect_regions(self, AERoom.W8L2Lava.value, AERoom.Coin59.value,
                        lambda state: SF_MechRoom(state, self))
        # 8-3
        connect_regions(self, AERoom.W8L3Water.value, AERoom.Coin64.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W8L3Tank.value, AERoom.Coin66.value,
                        lambda state: TVT_TankRoom(state, self))
        # 9-1
        connect_regions(self, AERoom.W9L1Entry.value, AERoom.Coin73.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Entry.value, AERoom.Coin74.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Haunted.value, AERoom.Coin75.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Western.value, AERoom.Coin77.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Crater.value, AERoom.Coin78.value,
                        lambda state: MM_SHA(state, self) and HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Outside.value, AERoom.Coin79.value,
                        lambda state: MM_SHA(state, self))
        connect_regions(self, AERoom.W9L1Castle.value, AERoom.Coin80.value,
                        lambda state: MM_UFODoor(state, self))
        connect_regions(self, AERoom.W9L1Head.value, AERoom.Coin84.value,
                        lambda state: MM_DoubleDoor(state, self))
        connect_regions(self, AERoom.W9L1Side.value, AERoom.Coin85.value,
                        lambda state: MM_SHA(state, self) and HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Climb2.value, AERoom.Coin82.value,
                        lambda state: MM_SpaceMonkeys(state, self))


    # Mailboxes
    if self.options.mailbox == "true" or (self.options.shufflenet == "true" and self.options.coin == "true"):
        # Time Station
        connect_regions(self, AERoom.TimeStationMain.value, AERoom.Mailbox59.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationMain.value, AERoom.Mailbox60.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationMinigame.value, AERoom.Mailbox61.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationTraining.value, AERoom.Mailbox62.value, 
                        lambda state: NoRequirement())

    if self.options.mailbox == "true":
        # 1-1
        connect_regions(self, AERoom.W1L1Main.value, AERoom.Mailbox1.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L1Main.value, AERoom.Mailbox2.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L1Main.value, AERoom.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))
        # 1-2
        connect_regions(self, AERoom.W1L2Main.value, AERoom.Mailbox4.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AERoom.Mailbox5.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AERoom.Mailbox6.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AERoom.Mailbox7.value, 
                        lambda state: NoRequirement())
        # 1-3
        connect_regions(self, AERoom.W1L3Entry.value, AERoom.Mailbox8.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Entry.value, AERoom.Mailbox9.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W1L3Volcano.value, AERoom.Mailbox10.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Triceratops.value, AERoom.Mailbox11.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Triceratops.value, AERoom.Mailbox12.value,
                        lambda state: HasSling(state, self))
        # 2-1
        connect_regions(self, AERoom.W2L1Entry.value, AERoom.Mailbox13.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L1Entry.value, AERoom.Mailbox14.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.Mailbox15.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Mushroom.value, AERoom.Mailbox16.value,
                        lambda state: HasMobility(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AERoom.Mailbox17.value,
                        lambda state: TJ_FishEntry(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AERoom.Mailbox18.value,
                        lambda state: TJ_FishEntry(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AERoom.Mailbox19.value,
                        lambda state: TJ_FishEntry(state, self))
        connect_regions(self, AERoom.W2L1Tent.value, AERoom.Mailbox20.value,
                        lambda state: (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self) and CanHitOnce(state, self)) or (TJ_FishEntry(state, self) and CanHitMultiple(state, self)))
        connect_regions(self, AERoom.W2L1Boulder.value, AERoom.Mailbox21.value,
                        lambda state: (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self) and CanHitOnce(state, self)) or (TJ_FishEntry(state, self) and CanHitMultiple(state, self)))
        # 2-2
        connect_regions(self, AERoom.W2L2Outside.value, AERoom.Mailbox22.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Outside.value, AERoom.Mailbox23.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Outside.value, AERoom.Mailbox24.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Outside.value, AERoom.Mailbox25.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AERoom.Mailbox26.value,  
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AERoom.Mailbox27.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Obelisk.value, AERoom.Mailbox28.value,
                        lambda state: CanHitOnce(state, self))
        # 2-3
        connect_regions(self, AERoom.W2L3Outside.value, AERoom.Mailbox29.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L3Outside.value, AERoom.Mailbox30.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L3Main.value, AERoom.Mailbox31.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L3Main.value, AERoom.Mailbox32.value,
                        lambda state: CR_Inside(state, self) and CanSwim(state, self) and (HasMobility(state, self) or CanHitMultiple(state, self)))
        connect_regions(self, AERoom.W2L3Pillar.value, AERoom.Mailbox33.value,
                        lambda state: CR_Inside(state, self))
        # 4-1
        connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.Mailbox34.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.Mailbox35.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W4L1SecondRoom.value, AERoom.Mailbox36.value,
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
        # 4-2
        connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.Mailbox37.value,
                        lambda state: CanSwim(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L2SecondRoom.value, AERoom.Mailbox38.value,
                        lambda state: CanSwim(state, self) and CanHitOnce(state, self))
        # 4-3
        connect_regions(self, AERoom.W4L3Outside.value, AERoom.Mailbox39.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Outside.value, AERoom.Mailbox40.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Slide.value, AERoom.Mailbox41.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Gallery.value, AERoom.Mailbox42.value,
                        lambda state: CanHitOnce(state, self) and CanSwim(state, self))
        # 5-1
        connect_regions(self, AERoom.W5L1Main.value, AERoom.Mailbox43.value, 
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W5L1Main.value, AERoom.Mailbox44.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L1Main.value, AERoom.Mailbox45.value,
                        lambda state: CanHitMultiple(state, self))
        # 5-2
        connect_regions(self, AERoom.W5L2Caverns.value, AERoom.Mailbox46.value,
                        lambda state: HasFlyer(state, self) and CanHitOnce(state, self))
        # 5-3
        connect_regions(self, AERoom.W5L3Outside.value, AERoom.Mailbox47.value,
                        lambda state: HasFlyer(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L3Spring.value, AERoom.Mailbox48.value,
                        lambda state: HasFlyer(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L3Cave.value, AERoom.Mailbox49.value, 
                        lambda state: NoRequirement())
        # 7-1
        connect_regions(self, AERoom.W7L1Temple.value, AERoom.Mailbox50.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L1Temple.value, AERoom.Mailbox51.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L1Well.value, AERoom.Mailbox52.value,
                        lambda state: CanHitOnce(state, self))
        # 7-2
        connect_regions(self, AERoom.W7L2Gong.value, AERoom.Mailbox53.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L2Middle.value, AERoom.Mailbox54.value,
                        lambda state: (HasNet(state, self) or HasFlyer(state, self)) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L2Course.value, AERoom.Mailbox55.value,
                        lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self))
        # 7-3
        connect_regions(self, AERoom.W7L3Outside.value, AERoom.Mailbox56.value,
                        lambda state: CanHitOnce(state, self))
        # 8-2
        connect_regions(self, AERoom.W8L2Outside.value, AERoom.Mailbox57.value, 
                        lambda state: NoRequirement())
        # 9-1
        connect_regions(self, AERoom.W9L1Entry.value, AERoom.Mailbox58.value, 
                        lambda state: NoRequirement())


def Keys(state, world, count):
    return state.has(AEItem.Key.value, world.player, count)


def NoRequirement():
    return True


def CanHitOnce(state, world):
    return HasClub(state, world) or HasSling(state, world) or HasPunch(state, world)


def CanHitMultiple(state, world):
    return HasClub(state, world) or HasPunch(state, world)


def HasMobility(state, world):
    return HasFlyer(state, world)


def RCMonkey(state, world):
    return HasRC(state, world)


def CanSwim(state, world):
    return HasWaterNet(state, world)


def CanDive(state, world):
    return HasWaterNet(state, world)


def CanWaterCatch(state, world):
    return HasWaterNet(state, world)


def SuperFlyer(state, world):
    return False


def TJ_UFOEntry(state, world):
    return CanDive(state, world)


def TJ_UFOCliff(state, world):
    return HasFlyer(state, world)


def TJ_FishEntry(state, world):
    return CanSwim(state, world)


def TJ_Mushroom(state, world):
    return HasMobility(state, world) and CanHitMultiple(state, world)


def CR_Inside(state, world):
    return HasSling(state, world) or HasPunch(state, world)

def DI_SecondHalf(state, world):
    return CanHitOnce(state, world) and CanDive(state, world)


def DI_Boulders(state, world):
    return HasHoop(state, world) or HasRC(state, world)


def WSW_ThirdRoom(state, world):
    return (HasSling(state, world) and HasNet(state, world)) or HasFlyer(state, world)


def WSW_FourthRoom(state, world):
    return CanHitMultiple(state, world) or HasFlyer(state, world)


def CC_5Monkeys(state, world):
    return HasNet(state, world) and (HasClub(state, world) or HasFlyer(state, world) or HasPunch(state, world))


def CC_WaterRoom(state, world):
    return (HasNet(state, world) and CanHitMultiple(state, world)) or (CanDive(state, world) and HasPunch(state, world))


def CC_ButtonRoom(state, world):
    return CC_WaterRoom(state, world) and CanSwim(state, world)

def CP_FrontSewer(state, world):
    return HasNet(state, world) and HasRC(state, world)


def CP_FrontBarrels(state, world):
    return CP_FrontSewer(state, world) and (CanSwim(state, world) or HasMobility(state, world))


def CP_BackSewer(state, world):
    return False


def SF_CarRoom(state, world):
    return HasRC(state, world) or HasPunch(state, world)


def SF_MechRoom(state, world):
    return HasNet(state, world) and HasClub(state, world) and SF_CarRoom(state, world)


def TVT_HitButton(state, world):
    return HasFlyer(state, world) and CanHitOnce(state, world)


def TVT_TankRoom(state, world):
    return TVT_HitButton(state, world) and HasNet(state, world)

def TVT_BossRoom(state, world):
    return TVT_HitButton(state, world)


def MM_Natalie(state, world):
    return CanHitOnce(state, world) and HasNet(state, world)


def MM_Professor(state, world):
    return HasFlyer(state, world) and CanHitMultiple(state, world)


def Jake_Open(state, world):
    return MM_Natalie(state, world) and MM_Professor(state, world)


def MM_Jake(state, world):
    return (HasClub(state, world) or HasPunch(state, world)) and Jake_Open(state, world)


def MM_SHA(state, world):
    return MM_Natalie(state, world) and MM_Professor(state, world) and MM_Jake(state, world)


def MM_UFODoor(state, world):
    return MM_SHA(state, world) and HasNet(state, world) and HasSling(state, world)


def MM_DoubleDoor(state, world):
    return MM_UFODoor(state, world) and HasHoop(state, world) and HasRC(state, world) and CanHitMultiple(state, world)


def MM_SpaceMonkeys(state, world):
    return MM_DoubleDoor(state, world) and HasFlyer(state, world)


def MM_FinalBoss(state, world):
    return MM_DoubleDoor(state, world) and HasSling(state, world) and HasFlyer(state, world)


def HasClub(state, world):
    return state.has(AEItem.Club.value, world.player, 1)


def HasNet(state, world):
    return state.has(AEItem.Net.value, world.player, 1)


def HasRadar(state, world):
    return state.has(AEItem.Radar.value, world.player, 1)


def HasSling(state, world):
    return state.has(AEItem.Sling.value, world.player, 1)


def HasHoop(state, world):
    return state.has(AEItem.Hoop.value, world.player, 1)


def HasFlyer(state, world):
    return state.has(AEItem.Flyer.value, world.player, 1)


def HasRC(state, world):
    return state.has(AEItem.Car.value, world.player, 1)


def HasPunch(state, world):
    return state.has(AEItem.Punch.value, world.player, 1)


def HasWaterNet(state, world):
    return state.has(AEItem.WaterNet.value, world.player, 1)
