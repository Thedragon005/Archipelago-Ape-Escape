from .Regions import connect_regions, ApeEscapeLevel
from .Strings import AEItem, AERoom, AELocation


def set_noij_rules(self):
    # This is the logic for being able to catch every monkey to access the second Specter fight. The logic for the fight itself would be Sling + CanHitMultiple + Net.
    # Make sure to update this condition properly when alternate Peak Point Matrix unlock conditions are added.
    if self.options.goal == "second":
        connect_regions(self, "Menu", AERoom.W9L2Boss.value,
                        lambda state: Keys(state, self, self.levellist[21].keys) and HasNet(state, self) and HasSling(
                            state, self) and HasHoop(state, self) and HasFlyer(state, self) and CanHitMultiple(state,
                                                                                                               self) and HasRC(
                            state, self) and CanDive(state, self) and CanWaterCatch(state, self))

    # Time Station
    connect_regions(self, "Menu", AERoom.TimeStationMain.value, lambda state: True)
    connect_regions(self, "Menu", AERoom.TimeStationMinigame.value, lambda state: True)
    connect_regions(self, "Menu", AERoom.TimeStationTraining.value, lambda state: True)

    # 1-1
    connect_regions(self, "Menu", AERoom.W1L1Main.value, lambda state: Keys(state, self, self.levellist[0].keys))

    connect_regions(self, AERoom.W1L1Main.value, AELocation.W1L1Noonan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AELocation.W1L1Jorjy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AELocation.W1L1Nati.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L1Main.value, AELocation.W1L1TrayC.value,
                    lambda state: HasNet(state, self))

    # 1-2
    connect_regions(self, "Menu", AERoom.W1L2Main.value, lambda state: Keys(state, self, self.levellist[1].keys))

    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2Shay.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2DrMonk.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2Ahchoo.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2Grunt.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2Tyrone.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L2Main.value, AELocation.W1L2Gornif.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))

    # 1-3
    connect_regions(self, "Menu", AERoom.W1L3Entry.value, lambda state: Keys(state, self, self.levellist[2].keys))
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Volcano.value, lambda state: True)
    connect_regions(self, AERoom.W1L3Entry.value, AERoom.W1L3Triceratops.value, lambda state: True)

    connect_regions(self, AERoom.W1L3Entry.value, AELocation.W1L3Scotty.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AELocation.W1L3Coco.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AELocation.W1L3JThomas.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W1L3Entry.value, AELocation.W1L3Moggan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Volcano.value, AELocation.W1L3Barney.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Volcano.value, AELocation.W1L3Mattie.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W1L3Triceratops.value, AELocation.W1L3Rocky.value,
                    lambda state: HasSling(state, self) and HasNet(state, self))

    # 2-1
    connect_regions(self, "Menu", AERoom.W2L1Entry.value, lambda state: Keys(state, self, self.levellist[3].keys))
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Mushroom.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Fish.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Fish.value, AERoom.W2L1Tent.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Tent.value, AERoom.W2L1Boulder.value, lambda state: True)
    connect_regions(self, AERoom.W2L1Entry.value, AERoom.W2L1Boulder.value, lambda state: True)

    connect_regions(self, AERoom.W2L1Entry.value, AELocation.W2L1Marquez.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L1Entry.value, AELocation.W2L1Livinston.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Entry.value, AELocation.W2L1George.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.W2L1Gonzo.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.W2L1Zanzibar.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.W2L1Alphonse.value,
                    lambda state: TJ_Mushroom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AELocation.W2L1Maki.value,
                    lambda state: TJ_FishEntry(state, self) and (
                                HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AELocation.W2L1Herb.value,
                    lambda state: TJ_FishEntry(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Fish.value, AELocation.W2L1Dilweed.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (
                                TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AELocation.W2L1Stoddy.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (
                                TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AELocation.W2L1Mitong.value,
                    lambda state: ((TJ_FishEntry(state, self) and CanHitMultiple(state, self)) or (
                                TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Tent.value, AELocation.W2L1Nasus.value,
                    lambda state: (TJ_FishEntry(state, self) or (
                                TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self))) and CanHitMultiple(state,
                                                                                                           self) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W2L1Boulder.value, AELocation.W2L1Elehcim.value,
                    lambda state: (TJ_UFOEntry(state, self) or (
                                TJ_FishEntry(state, self) and CanHitMultiple(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L1Boulder.value, AELocation.W2L1Selur.value,
                    lambda state: ((TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self)) or (
                                TJ_FishEntry(state, self) and CanHitMultiple(state, self))) and (
                                              HasClub(state, self) or HasSling(state, self) or HasFlyer(state,
                                                                                                        self)) and HasNet(
                        state, self))

    # 2-2
    connect_regions(self, "Menu", AERoom.W2L2Outside.value, lambda state: Keys(state, self, self.levellist[4].keys))
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Fan.value, lambda state: True)
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Obelisk.value, lambda state: True)
    connect_regions(self, AERoom.W2L2Outside.value, AERoom.W2L2Water.value, lambda state: True)

    connect_regions(self, AERoom.W2L2Outside.value, AELocation.W2L2Kyle.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AELocation.W2L2Stan.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AELocation.W2L2Kenny.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AELocation.W2L2Cratman.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Outside.value, AELocation.W2L2Mooshy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Fan.value, AELocation.W2L2Nuzzy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Fan.value, AELocation.W2L2Mav.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AELocation.W2L2Papou.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AELocation.W2L2Trance.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L2Obelisk.value, AELocation.W2L2Bernt.value,
                    lambda state: (HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AELocation.W2L2Runt.value,
                    lambda state: ((CanSwim(state, self) and CanHitOnce(state, self)) or HasSling(state,
                                                                                                  self) or HasHoop(
                        state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AELocation.W2L2Hoolah.value,
                    lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L2Water.value, AELocation.W2L2Chino.value,
                    lambda state: ((CanSwim(state, self) and CanHitOnce(state, self)) or HasSling(state,
                                                                                                  self) or HasHoop(
                        state, self)) and HasNet(state, self))

    # 2-3
    connect_regions(self, "Menu", AERoom.W2L3Outside.value, lambda state: Keys(state, self, self.levellist[5].keys))
    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Side.value, lambda state: True)
    connect_regions(self, AERoom.W2L3Outside.value, AERoom.W2L3Main.value, lambda state: True)
    connect_regions(self, AERoom.W2L3Main.value, AERoom.W2L3Pillar.value, lambda state: True)

    connect_regions(self, AERoom.W2L3Outside.value, AELocation.W2L3Bazzle.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L3Outside.value, AELocation.W2L3Freeto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W2L3Side.value, AELocation.W2L3Troopa.value,
                    lambda state: (HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W2L3Main.value, AELocation.W2L3Stymie.value,
                    lambda state: CR_Inside(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Main.value, AELocation.W2L3Spanky.value,
                    lambda state: CR_Inside(state, self) and ((CanSwim(state, self) and (
                                HasMobility(state, self) or CanHitMultiple(state, self))) or HasFlyer(state,
                                                                                                      self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W2L3Main.value, AELocation.W2L3Jesta.value,
                    lambda state: CR_Inside(state, self) and (CanHitMultiple(state, self) or (
                                CanSwim(state, self) and HasMobility(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Pillar.value, AELocation.W2L3Pally.value,
                    lambda state: CR_Inside(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W2L3Pillar.value, AELocation.W2L3Crash.value,
                    lambda state: CR_Inside(state, self) and (
                                RCMonkey(state, self) or SuperFlyer(state, self)) and HasNet(state, self))

    # 4-1
    connect_regions(self, "Menu", AERoom.W4L1FirstRoom.value, lambda state: Keys(state, self, self.levellist[7].keys))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AERoom.W4L1SecondRoom.value, lambda state: True)

    connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.W4L1CoolBlue.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.W4L1Sandy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.W4L1ShellE.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.W4L1Gidget.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.W4L1Shaka.value,
                    lambda state: CB_Lamp(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.W4L1Puka.value,
                    lambda state: CB_Lamp(state, self) and (
                                CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.W4L1MaxMahalo.value,
                    lambda state: CB_Lamp(state, self) and (
                                HasHoop(state, self) or (HasSling(state, self) and HasFlyer(state, self))) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.W4L1Moko.value,
                    lambda state: CB_Lamp(state, self) and HasFlyer(state, self) and HasNet(state, self))

    # 4-2
    connect_regions(self, "Menu", AERoom.W4L2FirstRoom.value, lambda state: Keys(state, self, self.levellist[8].keys))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AERoom.W4L2SecondRoom.value, lambda state: True)

    connect_regions(self, AERoom.W4L2FirstRoom.value, AELocation.W4L2Chip.value,
                    lambda state: CanSwim(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AELocation.W4L2Oreo.value,
                    lambda state: HasMobility(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AELocation.W4L2Puddles.value,
                    lambda state: (CanDive(state, self) or (HasHoop(state, self) and HasFlyer(state, self))) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W4L2FirstRoom.value, AELocation.W4L2Kalama.value,
                    lambda state: HasMobility(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.W4L2Iz.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.W4L2BongBong.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.W4L2Jux.value,
                    lambda state: CanSwim(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.W4L2Pickles.value,
                    lambda state: CanSwim(state, self) and CanHitMultiple(state, self) and HasNet(state, self))

    # 4-3
    connect_regions(self, "Menu", AERoom.W4L3Outside.value, lambda state: Keys(state, self, self.levellist[9].keys))
    connect_regions(self, AERoom.W4L3Outside.value, AERoom.W4L3Stomach.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Stomach.value, AERoom.W4L3Slide.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Slide.value, AERoom.W4L3Gallery.value, lambda state: True)
    connect_regions(self, AERoom.W4L3Gallery.value, AERoom.W4L3Tentacle.value, lambda state: True)

    connect_regions(self, AERoom.W4L3Outside.value, AELocation.W4L3TonTon.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Outside.value, AELocation.W4L3Stuw.value,
                    lambda state: (CanSwim(state, self) or CanHitOnce(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Stomach.value, AELocation.W4L3Mars.value,
                    lambda state: HasRC(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W4L3Stomach.value, AELocation.W4L3Murky.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Stomach.value, AELocation.W4L3Horke.value,
                    lambda state: (CanHitOnce(state, self) and (
                                CanSwim(state, self) or HasFlyer(state, self))) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AELocation.W4L3Howeerd.value,
                    lambda state: DI_SecondHalf(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AELocation.W4L3Robbin.value,
                    lambda state: DI_SecondHalf(state, self) and HasSling(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AELocation.W4L3Jakkee.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AELocation.W4L3Frederic.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Gallery.value, AELocation.W4L3Baba.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W4L3Tentacle.value, AELocation.W4L3Quirck.value,
                    lambda state: DI_SecondHalf(state, self) and DI_Boulders(state, self) and DI_Lamp(state,
                                                                                                      self) and HasNet(
                        state, self))

    # 5-1
    connect_regions(self, "Menu", AERoom.W5L1Main.value, lambda state: Keys(state, self, self.levellist[10].keys))

    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Popcicle.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Iced.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Rickets.value,
                    lambda state: (HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Skeens.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Chilly.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L1Main.value, AELocation.W5L1Denggoy.value,
                    lambda state: HasNet(state, self))

    # 5-2
    connect_regions(self, "Menu", AERoom.W5L2Entry.value, lambda state: Keys(state, self, self.levellist[11].keys))
    connect_regions(self, AERoom.W5L2Caverns.value, AERoom.W5L2Water.value, lambda state: True)
    connect_regions(self, AERoom.W5L2Entry.value, AERoom.W5L2Caverns.value, lambda state: True)

    connect_regions(self, AERoom.W5L2Entry.value, AELocation.W5L2Storm.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L2Entry.value, AELocation.W5L2Qube.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AELocation.W5L2Ranix.value,
                    lambda state: (CanSwim(state, self) and HasNet(state, self)) or (
                                (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and (
                                    HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self)))))
    connect_regions(self, AERoom.W5L2Water.value, AELocation.W5L2Sharpe.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AELocation.W5L2Sticky.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L2Water.value, AELocation.W5L2Droog.value,
                    lambda state: (CanDive(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W5L2Caverns.value, AELocation.W5L2Gash.value,
                    lambda state: HasNet(state, self) or CanWaterCatch(state, self))
    connect_regions(self, AERoom.W5L2Caverns.value, AELocation.W5L2Kundra.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L2Caverns.value, AELocation.W5L2Shadow.value,
                    lambda state: HasNet(state, self))

    # 5-3
    connect_regions(self, "Menu", AERoom.W5L3Outside.value, lambda state: Keys(state, self, self.levellist[12].keys))
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Spring.value, lambda state: True)
    connect_regions(self, AERoom.W5L3Outside.value, AERoom.W5L3Cave.value, lambda state: True)

    connect_regions(self, AERoom.W5L3Outside.value, AELocation.W5L3Punky.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AELocation.W5L3Ameego.value,
                    lambda state: CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AELocation.W5L3Yoky.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Outside.value, AELocation.W5L3Jory.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AELocation.W5L3Crank.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AELocation.W5L3Claxter.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Spring.value, AELocation.W5L3Looza.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Cave.value, AELocation.W5L3Roti.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W5L3Cave.value, AELocation.W5L3Dissa.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))

    # 7-1
    connect_regions(self, "Menu", AERoom.W7L1Outside.value, lambda state: Keys(state, self, self.levellist[14].keys))
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Temple.value, lambda state: True)
    connect_regions(self, AERoom.W7L1Outside.value, AERoom.W7L1Well.value, lambda state: True)

    connect_regions(self, AERoom.W7L1Outside.value, AELocation.W7L1Taku.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AELocation.W7L1Rocka.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AELocation.W7L1Maralea.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Outside.value, AELocation.W7L1Wog.value,
                    lambda state: (HasClub(state, self) or HasSling(state, self) or HasFlyer(state, self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AELocation.W7L1Mayi.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AELocation.W7L1Owyang.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AELocation.W7L1Long.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AELocation.W7L1Elly.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Temple.value, AELocation.W7L1Chunky.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L1Well.value, AELocation.W7L1Voti.value,
                    lambda state: (HasSling(state, self) or (
                                HasHoop(state, self) and HasFlyer(state, self)) or SuperFlyer(state, self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W7L1Well.value, AELocation.W7L1QuelTin.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L1Well.value, AELocation.W7L1Phaldo.value,
                    lambda state: HasNet(state, self))

    # 7-2
    connect_regions(self, "Menu", AERoom.W7L2First.value, lambda state: Keys(state, self, self.levellist[15].keys))
    connect_regions(self, AERoom.W7L2First.value, AERoom.W7L2Gong.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Gong.value, AERoom.W7L2Middle.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Middle.value, AERoom.W7L2Course.value, lambda state: True)
    connect_regions(self, AERoom.W7L2Course.value, AERoom.W7L2Barrel.value, lambda state: True)

    connect_regions(self, AERoom.W7L2First.value, AELocation.W7L2Minky.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2First.value, AELocation.W7L2Zobbro.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AELocation.W7L2Xeeto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AELocation.W7L2Moops.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Gong.value, AELocation.W7L2Zanabi.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L2Middle.value, AELocation.W7L2Doxs.value,
                    lambda state: WSW_ThirdRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Course.value, AELocation.W7L2Buddha.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Course.value, AELocation.W7L2Fooey.value,
                    lambda state: WSW_ThirdRoom(state, self) and RCMonkey(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Barrel.value, AELocation.W7L2Kong.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and (
                                HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W7L2Barrel.value, AELocation.W7L2Phool.value,
                    lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self) and (
                                HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(
                        state, self))

    # 7-3
    connect_regions(self, "Menu", AERoom.W7L3Outside.value, lambda state: Keys(state, self, self.levellist[16].keys))
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Castle.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Bell.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Castle.value, AERoom.W7L3Elevator.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Elevator.value, AERoom.W7L3Basement.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Basement.value, AERoom.W7L3Button.value, lambda state: True)
    connect_regions(self, AERoom.W7L3Outside.value, AERoom.W7L3Boss.value,
                    lambda state: CanHitMultiple(state, self) and CC_ButtonRoom(state, self))

    connect_regions(self, AERoom.W7L3Outside.value, AELocation.W7L3Robart.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AELocation.W7L3Igor.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AELocation.W7L3Naners.value,
                    lambda state: HasNet(state, self))
    # CC_5Monkeys access rule specifically checks for the ability to catch 5 monkeys, so Net is already part of that check.
    connect_regions(self, AERoom.W7L3Outside.value, AELocation.W7L3Neeners.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Outside.value, AELocation.W7L3Charles.value,
                    lambda state: HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AELocation.W7L3Gustav.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AELocation.W7L3Wilhelm.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AELocation.W7L3Emmanuel.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Castle.value, AELocation.W7L3SirCutty.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AELocation.W7L3Calligan.value,
                    lambda state: CC_WaterRoom(state, self) and (
                                CanDive(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AELocation.W7L3Castalist.value,
                    lambda state: CC_WaterRoom(state, self) and CanDive(state, self) and CanWaterCatch(state, self))
    connect_regions(self, AERoom.W7L3Basement.value, AELocation.W7L3Deveneom.value,
                    lambda state: CC_ButtonRoom(state, self) and (HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W7L3Button.value, AELocation.W7L3Astur.value,
                    lambda state: CC_ButtonRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W7L3Button.value, AELocation.W7L3Kilserack.value,
                    lambda state: CC_ButtonRoom(state, self) and (
                                HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self))))
    connect_regions(self, AERoom.W7L3Elevator.value, AELocation.W7L3Ringo.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Elevator.value, AELocation.W7L3Densil.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Elevator.value, AELocation.W7L3Figero.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AELocation.W7L3Fej.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AELocation.W7L3Joey.value,
                    lambda state: CC_5Monkeys(state, self))
    connect_regions(self, AERoom.W7L3Bell.value, AELocation.W7L3Donqui.value,
                    lambda state: HasNet(state, self))

    # 8-1
    connect_regions(self, "Menu", AERoom.W8L1Outside.value, lambda state: Keys(state, self, self.levellist[17].keys))
    connect_regions(self, AERoom.W8L1Outside.value, AERoom.W8L1Sewers.value, lambda state: True)
    connect_regions(self, AERoom.W8L1Sewers.value, AERoom.W8L1Barrel.value, lambda state: True)

    connect_regions(self, AERoom.W8L1Outside.value, AELocation.W8L1Kaine.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AELocation.W8L1Jaxx.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AELocation.W8L1Gehry.value,
                    lambda state: ((CP_FrontBarrels(state, self) and CanDive(state, self)) or HasFlyer(state,
                                                                                                       self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W8L1Outside.value, AELocation.W8L1Alcatraz.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AELocation.W8L1Tino.value,
                    lambda state: ((CP_FrontSewer(state, self) or CP_BackSewer(state, self)) and HasRC(state,
                                                                                                       self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AELocation.W8L1QBee.value,
                    lambda state: ((CP_FrontSewer(state, self) and HasRC(state, self)) or CP_BackSewer(state,
                                                                                                       self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W8L1Sewers.value, AELocation.W8L1McManic.value,
                    lambda state: (((CP_FrontSewer(state, self) or CP_BackSewer(state, self)) and HasRC(state,
                                                                                                        self)) or HasFlyer(
                        state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1Dywan.value,
                    lambda state: (CP_FrontBarrels(state, self) or CP_BackSewer(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1CKHutch.value,
                    lambda state: ((CP_FrontBarrels(state, self) or CP_BackSewer(state, self)) and CanDive(state,
                                                                                                           self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1Winky.value,
                    lambda state: (CP_FrontBarrels(state, self) or CP_BackSewer(state, self)) and (
                                HasNet(state, self) or (CanDive(state, self) and CanWaterCatch(state, self))))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1BLuv.value,
                    lambda state: ((CP_FrontBarrels(state, self) and (
                                CanSwim(state, self) or HasFlyer(state, self))) or CP_BackSewer(state,
                                                                                                self)) and HasNet(state,
                                                                                                                  self))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1Camper.value,
                    lambda state: ((CP_FrontBarrels(state, self) or CP_BackSewer(state, self)) and CanDive(state,
                                                                                                           self)) and (
                                              HasNet(state, self) or CanWaterCatch(state, self)))
    connect_regions(self, AERoom.W8L1Barrel.value, AELocation.W8L1Huener.value,
                    lambda state: ((CP_FrontBarrels(state, self) and (
                                HasHoop(state, self) or CanSwim(state, self)) and HasFlyer(state,
                                                                                           self)) or CP_BackSewer(state,
                                                                                                                  self)) and HasNet(
                        state, self))

    # 8-2
    connect_regions(self, "Menu", AERoom.W8L2Outside.value, lambda state: Keys(state, self, self.levellist[18].keys))
    connect_regions(self, AERoom.W8L2Outside.value, AERoom.W8L2Factory.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2RC.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2Wheel.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Factory.value, AERoom.W8L2Mech.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Mech.value, AERoom.W8L2Lava.value, lambda state: True)
    connect_regions(self, AERoom.W8L2Lava.value, AERoom.W8L2Conveyor.value, lambda state: True)

    connect_regions(self, AERoom.W8L2Outside.value, AELocation.W8L2BigShow.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L2Outside.value, AELocation.W8L2Dreos.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L2Factory.value, AELocation.W8L2Reznor.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2RC.value, AELocation.W8L2Urkel.value,
                    lambda state: (SF_CarRoom(state, self) or HasSling(state, self) or SuperFlyer(state,
                                                                                                  self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AELocation.W8L2VanillaS.value,
                    lambda state: SF_MechRoom(state, self) and HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AELocation.W8L2Radd.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Lava.value, AELocation.W8L2Shimbo.value,
                    lambda state: SF_MechRoom(state, self) and RCMonkey(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Conveyor.value, AELocation.W8L2Hurt.value,
                    lambda state: SF_MechRoom(state, self) and CanHitMultiple(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Conveyor.value, AELocation.W8L2String.value,
                    lambda state: SF_MechRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L2Mech.value, AELocation.W8L2Khamo.value,
                    lambda state: SF_MechRoom(state, self) and CanHitMultiple(state, self) and HasNet(state, self))

    # 8-3
    connect_regions(self, "Menu", AERoom.W8L3Outside.value, lambda state: Keys(state, self, self.levellist[19].keys))
    connect_regions(self, AERoom.W8L3Outside.value, AERoom.W8L3Lobby.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Water.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Lobby.value, AERoom.W8L3Tank.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Fan.value, lambda state: True)
    connect_regions(self, AERoom.W8L3Tank.value, AERoom.W8L3Boss.value,
                    lambda state: TVT_BossRoom(state, self) and (
                                HasSling(state, self) or (HasFlyer(state, self) and HasRC(state, self))))

    connect_regions(self, AERoom.W8L3Outside.value, AELocation.W8L3Fredo.value,
                    lambda state: HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Water.value, AELocation.W8L3Charlee.value,
                    lambda state: TVT_HitButton(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Water.value, AELocation.W8L3Mach3.value,
                    lambda state: TVT_HitButton(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Lobby.value, AELocation.W8L3Tortuss.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W8L3Lobby.value, AELocation.W8L3Manic.value,
                    lambda state: HasFlyer(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AELocation.W8L3Ruptdis.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AELocation.W8L3Eighty7.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Tank.value, AELocation.W8L3Danio.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AELocation.W8L3Roosta.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AELocation.W8L3Tellis.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AELocation.W8L3Whack.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W8L3Fan.value, AELocation.W8L3Frostee.value,
                    lambda state: TVT_TankRoom(state, self) and HasNet(state, self))

    # 9-1
    connect_regions(self, "Menu", AERoom.W9L1Hub.value, lambda state: Keys(state, self, self.levellist[20].keys))
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

    connect_regions(self, AERoom.W9L1Entry.value, AELocation.W9L1Goopo.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Haunted.value, AELocation.W9L1Porto.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AELocation.W9L1Slam.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AELocation.W9L1Junk.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Coffin.value, AELocation.W9L1Crib.value,
                    lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AELocation.W9L1Nak.value,
                    lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AELocation.W9L1Cloy.value,
                    lambda state: HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AELocation.W9L1Shaw.value,
                    lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Western.value, AELocation.W9L1Flea.value,
                    lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Crater.value, AELocation.W9L1Schafette.value,
                    lambda state: MM_SHA(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Outside.value, AELocation.W9L1Donovan.value,
                    lambda state: MM_UFOMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Outside.value, AELocation.W9L1Laura.value,
                    lambda state: MM_UFOMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AELocation.W9L1Uribe.value,
                    lambda state: MM_UFODoor(state, self) and HasPunch(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AELocation.W9L1Gordo.value,
                    lambda state: MM_UFODoor(state, self) and (HasRC(state, self) or HasFlyer(state, self)) and HasNet(
                        state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AELocation.W9L1Raeski.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Castle.value, AELocation.W9L1Poopie.value,
                    lambda state: MM_UFODoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb1.value, AELocation.W9L1Teacup.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb1.value, AELocation.W9L1Shine.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb2.value, AELocation.W9L1Wrench.value,
                    lambda state: MM_SpaceMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Climb2.value, AELocation.W9L1Bronson.value,
                    lambda state: MM_SpaceMonkeys(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AELocation.W9L1Bungee.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AELocation.W9L1Carro.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Head.value, AELocation.W9L1Carlito.value,
                    lambda state: MM_DoubleDoor(state, self) and HasNet(state, self))
    connect_regions(self, AERoom.W9L1Side.value, AELocation.W9L1BG.value,
                    lambda state: MM_SHA(state, self) and (HasSling(state, self) or HasFlyer(state, self)) and HasNet(
                        state, self))

    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player, 1)

    if self.options.coin == "true":
        # Coins
        # 1-1
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Coin1.value,
                        lambda state: NoRequirement())
        # 1-2
        connect_regions(self, AERoom.W1L2Main.value, AELocation.Coin2.value,
                        lambda state: CanDive(state, self))
        # 1-3
        connect_regions(self, AERoom.W1L3Entry.value, AELocation.Coin3.value,
                        lambda state: NoRequirement())
        # 2-1
        connect_regions(self, AERoom.W2L1Entry.value, AELocation.Coin6.value,
                        lambda state: HasMobility(state, self))
        connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.Coin7.value,
                        lambda state: TJ_Mushroom(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AELocation.Coin8.value,
                        lambda state: (TJ_FishEntry(state, self)))
        connect_regions(self, AERoom.W2L1Tent.value, AELocation.Coin9.value,
                        lambda state: (TJ_FishEntry(state, self) and (CanHitMultiple(state, self))) or (
                                    (TJ_UFOEntry(state, self)) and (TJ_UFOCliff(state, self))))
        # 2-2
        connect_regions(self, AERoom.W2L2Outside.value, AELocation.Coin11.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AELocation.Coin12.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Obelisk.value, AELocation.Coin13.value,
                        lambda state: (HasHoop(state, self) and HasFlyer(state, self)) or HasRC(state,
                                                                                                self) or HasPunch(state,
                                                                                                                  self))
        connect_regions(self, AERoom.W2L2Water.value, AELocation.Coin14.value,
                        lambda state: CanDive(state, self) and CanHitOnce(state, self))
        # 2-3
        connect_regions(self, AERoom.W2L3Main.value, AELocation.Coin17.value,
                        lambda state: CR_Inside(state, self) and (CanSwim(state, self) or HasMobility(state, self)))
        # 3-1
        connect_regions(self, "Menu", AERoom.W3L1Coin19.value,
                        lambda state: CanSwim(state, self) and Keys(state, self, self.levellist[6].keys))
        # 4-1
        connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.Coin21.value,
                        lambda state: CB_Lamp(state, self))
        # 4-2
        connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.Coin23.value,
                        lambda state: CanDive(state, self) or (CanSwim(state, self) and HasRC(state, self)))
        # 4-3
        connect_regions(self, AERoom.W4L3Outside.value, AELocation.Coin24.value,
                        lambda state: CanSwim(state, self) or CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Stomach.value, AELocation.Coin25.value,
                        lambda state: CanDive(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Slide.value, AELocation.Coin28.value,
                        lambda state: ((CanHitOnce(state, self) and HasNet(state, self)) or HasPunch(state, self)))
        # 5-1
        connect_regions(self, AERoom.W5L1Main.value, AELocation.Coin29.value,
                        lambda state: NoRequirement())
        # 5-2
        connect_regions(self, AERoom.W5L2Entry.value, AELocation.Coin30.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W5L2Water.value, AELocation.Coin31.value,
                        lambda state: CanDive(state, self))
        connect_regions(self, AERoom.W5L2Caverns.value, AELocation.Coin32.value,
                        lambda state: NoRequirement())
        # 5-3
        connect_regions(self, AERoom.W5L3Spring.value, AELocation.Coin34.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W5L3Cave.value, AELocation.Coin35.value,
                        lambda state: CanHitOnce(state, self))
        # 6-1
        connect_regions(self, "Menu", AERoom.W6L1Coin36.value,
                        lambda state: HasFlyer(state, self) and Keys(state, self, self.levellist[13].keys))
        # 7-1
        connect_regions(self, AERoom.W7L1Outside.value, AELocation.Coin37.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L1Temple.value, AELocation.Coin38.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L1Well.value, AELocation.Coin39.value,
                        lambda state: HasFlyer(state, self))
        # 7-2
        connect_regions(self, AERoom.W7L2First.value, AELocation.Coin40.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W7L2Gong.value, AELocation.Coin41.value,
                        lambda state: HasNet(state, self))
        connect_regions(self, AERoom.W7L2Barrel.value, AELocation.Coin44.value,
                        lambda state: HasFlyer(state, self))
        # 7-3
        connect_regions(self, AERoom.W7L3Outside.value, AELocation.Coin45.value,
                        lambda state: HasClub(state, self) or HasSling(state, self) or HasHoop(state, self) or HasFlyer(
                            state, self) or HasPunch(state, self))
        connect_regions(self, AERoom.W7L3Castle.value, AELocation.Coin46.value,
                        lambda state: CC_5Monkeys(state, self))
        connect_regions(self, AERoom.W7L3Button.value, AELocation.Coin49.value,
                        lambda state: CC_ButtonRoom(state, self))
        connect_regions(self, AERoom.W7L3Elevator.value, AELocation.Coin50.value,
                        lambda state: CC_5Monkeys(state, self) or CC_WaterRoom(state, self) or (
                                    HasHoop(state, self) and HasFlyer(state, self)))
        # 8-1
        connect_regions(self, AERoom.W8L1Outside.value, AELocation.Coin53.value,
                        lambda state: (CP_FrontBarrels(state, self) and CanDive(state, self)) or HasFlyer(state, self))
        connect_regions(self, AERoom.W8L1Sewers.value, AELocation.Coin54.value,
                        lambda state: (CP_FrontSewer(state, self) and (
                                    HasRC(state, self) or SuperFlyer(state, self))) or (
                                                  CP_BackSewer(state, self) and HasRC(state, self)))
        connect_regions(self, AERoom.W8L1Barrel.value, AELocation.Coin55.value,
                        lambda state: (CP_FrontBarrels(state, self) or CP_BackSewer(state, self)) and HasFlyer(state,
                                                                                                               self))
        # 8-2
        connect_regions(self, AERoom.W8L2RC.value, AELocation.Coin58.value,
                        lambda state: SF_CarRoom(state, self) or SuperFlyer(state, self))
        connect_regions(self, AERoom.W8L2Lava.value, AELocation.Coin59.value,
                        lambda state: SF_MechRoom(state, self))
        # 8-3
        connect_regions(self, AERoom.W8L3Water.value, AELocation.Coin64.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W8L3Tank.value, AELocation.Coin66.value,
                        lambda state: TVT_TankRoom(state, self))
        # 9-1
        connect_regions(self, AERoom.W9L1Entry.value, AELocation.Coin73.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Entry.value, AELocation.Coin74.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Haunted.value, AELocation.Coin75.value,
                        lambda state: HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Western.value, AELocation.Coin77.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W9L1Crater.value, AELocation.Coin78.value,
                        lambda state: MM_SHA(state, self) and HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Outside.value, AELocation.Coin79.value,
                        lambda state: MM_SHA(state, self))
        connect_regions(self, AERoom.W9L1Castle.value, AELocation.Coin80.value,
                        lambda state: MM_UFODoor(state, self))
        connect_regions(self, AERoom.W9L1Head.value, AELocation.Coin84.value,
                        lambda state: MM_DoubleDoor(state, self))
        connect_regions(self, AERoom.W9L1Side.value, AELocation.Coin85.value,
                        lambda state: MM_SHA(state, self) and HasFlyer(state, self))
        connect_regions(self, AERoom.W9L1Climb2.value, AELocation.Coin82.value,
                        lambda state: MM_SpaceMonkeys(state, self))

    # Mailboxes
    if self.options.mailbox == "true" or (self.options.shufflenet == "true" and self.options.coin == "true"):
        # Time Station
        connect_regions(self, AERoom.TimeStationMain.value, AELocation.Mailbox60.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationMain.value, AELocation.Mailbox61.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationMinigame.value, AELocation.Mailbox62.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.TimeStationTraining.value, AELocation.Mailbox63.value,
                        lambda state: NoRequirement())

    if self.options.mailbox == "true":
        # 1-1
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox1.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox2.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))
        # 1-2
        connect_regions(self, AERoom.W1L2Main.value, AELocation.Mailbox4.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AELocation.Mailbox5.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AELocation.Mailbox6.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L2Main.value, AELocation.Mailbox7.value,
                        lambda state: NoRequirement())
        # 1-3
        connect_regions(self, AERoom.W1L3Entry.value, AELocation.Mailbox8.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Entry.value, AELocation.Mailbox9.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W1L3Volcano.value, AELocation.Mailbox10.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Triceratops.value, AELocation.Mailbox11.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W1L3Triceratops.value, AELocation.Mailbox12.value,
                        lambda state: HasSling(state, self))
        # 2-1
        connect_regions(self, AERoom.W2L1Entry.value, AELocation.Mailbox13.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L1Entry.value, AELocation.Mailbox14.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.Mailbox15.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Mushroom.value, AELocation.Mailbox16.value,
                        lambda state: HasMobility(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AELocation.Mailbox17.value,
                        lambda state: TJ_FishEntry(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AELocation.Mailbox18.value,
                        lambda state: TJ_FishEntry(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L1Fish.value, AELocation.Mailbox19.value,
                        lambda state: TJ_FishEntry(state, self))
        connect_regions(self, AERoom.W2L1Tent.value, AELocation.Mailbox20.value,
                        lambda state: (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self) and CanHitOnce(state,
                                                                                                            self)) or (
                                                  TJ_FishEntry(state, self) and CanHitMultiple(state, self)))
        connect_regions(self, AERoom.W2L1Boulder.value, AELocation.Mailbox21.value,
                        lambda state: (TJ_UFOEntry(state, self) and TJ_UFOCliff(state, self) and CanHitOnce(state,
                                                                                                            self)) or (
                                                  TJ_FishEntry(state, self) and CanHitMultiple(state, self)))
        # 2-2
        connect_regions(self, AERoom.W2L2Outside.value, AELocation.Mailbox22.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Outside.value, AELocation.Mailbox23.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Outside.value, AELocation.Mailbox24.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Outside.value, AELocation.Mailbox25.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AELocation.Mailbox26.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L2Fan.value, AELocation.Mailbox27.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L2Obelisk.value, AELocation.Mailbox28.value,
                        lambda state: CanHitOnce(state, self))
        # 2-3
        connect_regions(self, AERoom.W2L3Outside.value, AELocation.Mailbox29.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L3Outside.value, AELocation.Mailbox30.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W2L3Main.value, AELocation.Mailbox31.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W2L3Main.value, AELocation.Mailbox32.value,
                        lambda state: CR_Inside(state, self) and CanSwim(state, self) and (
                                    HasMobility(state, self) or CanHitMultiple(state, self)))
        connect_regions(self, AERoom.W2L3Pillar.value, AELocation.Mailbox33.value,
                        lambda state: CR_Inside(state, self))
        # 4-1
        connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.Mailbox34.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L1FirstRoom.value, AELocation.Mailbox35.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W4L1SecondRoom.value, AELocation.Mailbox36.value,
                        lambda state: CanHitOnce(state, self) and CB_Lamp(state, self))
        # 4-2
        connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.Mailbox37.value,
                        lambda state: CanSwim(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L2SecondRoom.value, AELocation.Mailbox38.value,
                        lambda state: CanSwim(state, self) and CanHitOnce(state, self))
        # 4-3
        connect_regions(self, AERoom.W4L3Outside.value, AELocation.Mailbox39.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Outside.value, AELocation.Mailbox40.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Slide.value, AELocation.Mailbox41.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W4L3Gallery.value, AELocation.Mailbox42.value,
                        lambda state: CanHitOnce(state, self))
        # 5-1
        connect_regions(self, AERoom.W5L1Main.value, AELocation.Mailbox43.value,
                        lambda state: NoRequirement())
        connect_regions(self, AERoom.W5L1Main.value, AELocation.Mailbox44.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L1Main.value, AELocation.Mailbox45.value,
                        lambda state: NoRequirement())
        # 5-2
        connect_regions(self, AERoom.W5L2Caverns.value, AELocation.Mailbox46.value,
                        lambda state: CanHitOnce(state, self))
        # 5-3
        connect_regions(self, AERoom.W5L3Outside.value, AELocation.Mailbox47.value,
                        lambda state: HasFlyer(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L3Spring.value, AELocation.Mailbox48.value,
                        lambda state: HasFlyer(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W5L3Cave.value, AELocation.Mailbox49.value,
                        lambda state: NoRequirement())
        # 7-1
        connect_regions(self, AERoom.W7L1Temple.value, AELocation.Mailbox50.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L1Temple.value, AELocation.Mailbox51.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L1Well.value, AELocation.Mailbox52.value,
                        lambda state: CanHitOnce(state, self))
        # 7-2
        connect_regions(self, AERoom.W7L2Gong.value, AELocation.Mailbox53.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L2Middle.value, AELocation.Mailbox54.value,
                        lambda state: (HasNet(state, self) or HasFlyer(state, self)) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L2Middle.value, AELocation.Mailbox55.value,
                        lambda state: WSW_ThirdRoom(state, self) and CanHitOnce(state, self))
        connect_regions(self, AERoom.W7L2Course.value, AELocation.Mailbox56.value,
                        lambda state: WSW_ThirdRoom(state, self) and WSW_FourthRoom(state, self))
        # 7-3
        connect_regions(self, AERoom.W7L3Outside.value, AELocation.Mailbox57.value,
                        lambda state: CanHitOnce(state, self))
        # 8-2
        connect_regions(self, AERoom.W8L2Outside.value, AELocation.Mailbox58.value,
                        lambda state: NoRequirement())
        # 9-1
        connect_regions(self, AERoom.W9L1Entry.value, AELocation.Mailbox59.value,
                        lambda state: NoRequirement())


def Keys(state, world, count):
    return state.has(AEItem.Key.value, world.player, count)


def NoRequirement():
    return True


def CanHitOnce(state, world):
    return HasClub(state, world) or HasRadar(state, world) or HasSling(state, world) or HasHoop(state,
                                                                                                world) or HasFlyer(
        state, world) or HasRC(state, world) or HasPunch(state, world)


def CanHitMultiple(state, world):
    return HasClub(state, world) or HasSling(state, world) or HasHoop(state, world) or HasPunch(state, world)


def HasMobility(state, world):
    return HasHoop(state, world) or HasFlyer(state, world)


def RCMonkey(state, world):
    return HasSling(state, world) or HasRC(state, world)


def CanSwim(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 1))


def CanDive(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 2))


def CanWaterCatch(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or (
                state.has(AEItem.WaterCatch.value, world.player, 1) and state.has(AEItem.ProgWaterNet.value,
                                                                                  world.player, 1)))


def SuperFlyer(state, world):
    return HasFlyer(state, world) and (
                HasNet(state, world) or HasClub(state, world) or HasSling(state, world) or HasPunch(state,
                                                                                                    world)) and world.options.superflyer == "true"


def TJ_UFOEntry(state, world):
    return CanSwim(state, world)


def TJ_UFOCliff(state, world):
    return True


def TJ_FishEntry(state, world):
    return CanSwim(state, world) or HasFlyer(state, world)


def TJ_Mushroom(state, world):
    return (HasMobility(state, world) and CanHitMultiple(state, world)) or SuperFlyer(state, world)


def CR_Inside(state, world):
    return HasSling(state, world) or HasPunch(state, world)


def CB_Lamp(state, world):
    return state.has(AEItem.CB_Lamp.value, world.player, 1) and HasNet(state, world)


def DI_SecondHalf(state, world):
    return CanHitMultiple(state, world) and CanDive(state, world)


def DI_Lamp(state, world):
    return state.has(AEItem.DI_Lamp.value, world.player, 1) and HasNet(state, world)


def DI_Boulders(state, world):
    return HasHoop(state, world) or HasFlyer(state, world) or HasRC(state, world)


def WSW_ThirdRoom(state, world):
    return ((HasSling(state, world) or HasHoop(state, world)) and HasNet(state, world)) or HasFlyer(state, world)


def WSW_FourthRoom(state, world):
    return True


def CrC_Lamp(state, world):
    return state.has(AEItem.CrC_Lamp.value, world.player, 1) and HasNet(state, world)


def CC_5Monkeys(state, world):
    return CrC_Lamp(state, world) and (
                HasClub(state, world) or HasSling(state, world) or HasHoop(state, world) or HasFlyer(state,
                                                                                                     world) or HasPunch(
            state, world))


def CC_WaterRoom(state, world):
    return (CrC_Lamp(state, world) and CanHitMultiple(state, world)) or (
                CanSwim(state, world) and (HasFlyer(state, world) or HasPunch(state, world))) or (
                HasFlyer(state, world) or HasHoop(state, world)) or SuperFlyer(state, world)


def CC_ButtonRoom(state, world):
    return CC_WaterRoom(state, world) and (CanSwim(state, world) or HasFlyer(state, world))


def CP_Lamp(state, world):
    return state.has(AEItem.CP_Lamp.value, world.player, 1) and HasNet(state, world)


def CP_FrontSewer(state, world):
    return CP_Lamp(state, world) and HasRC(state, world)


def CP_FrontBarrels(state, world):
    return CP_FrontSewer(state, world) and (CanSwim(state, world) or HasMobility(state, world))


def CP_BackSewer(state, world):
    return HasFlyer(state, world) and CanDive(state, world)


def SF_Lamp(state, world):
    return state.has(AEItem.SF_Lamp.value, world.player, 1) and HasNet(state, world)


def SF_CarRoom(state, world):
    return (HasHoop(state, world) and HasFlyer(state, world)) or HasRC(state, world) or HasPunch(state, world)


def SF_MechRoom(state, world):
    return (HasHoop(state, world) and HasFlyer(state, world)) or (SF_Lamp(state, world) and (
                (HasClub(state, world) and (HasSling(state, world) or HasRC(state, world))) or HasPunch(state,
                                                                                                        world))) or SuperFlyer(
        state, world)


def TVT_Lobby_Lamp(state, world):
    return state.has(AEItem.TVT_Lobby_Lamp.value, world.player, 1) and HasNet(state, world)


def TVT_Tank_Lamp(state, world):
    return state.has(AEItem.TVT_Tank_Lamp.value, world.player, 1) and HasNet(state, world)


def TVT_HitButton(state, world):
    return HasClub(state, world) or HasSling(state, world) or HasFlyer(state, world)


def TVT_TankRoom(state, world):
    return TVT_HitButton(state, world) and TVT_Lobby_Lamp(state, world)


def TVT_BossRoom(state, world):
    return TVT_TankRoom(state, world) and TVT_Tank_Lamp(state, world)


def MM_Lamp(state, world):
    return state.has(AEItem.MM_Lamp.value, world.player, 1) and HasNet(state, world)


def MM_Natalie(state, world):
    return CanHitOnce(state, world) and HasNet(state, world)


def MM_Professor(state, world):
    return HasFlyer(state, world) and (HasClub(state, world) or HasSling(state, world) or HasPunch(state, world))


def Jake_Open(state, world):
    return True


def MM_Jake(state, world):
    return CanHitMultiple(state, world) and Jake_Open(state, world)


def MM_Lobby_DoubleDoor(state, world):
    return state.has(AEItem.MMLobbyDoubleDoorKey.value, world.player, 1)


def MM_SHA(state, world):
    return MM_Lobby_DoubleDoor(state, world)


def MM_UFOMonkeys(state, world):
    return MM_SHA(state, world) and HasNet(state, world) and (
                HasClub(state, world) or HasSling(state, world) or HasPunch(state, world))

def MM_UFODoor(state, world):
    return MM_UFOMonkeys(state, world) and MM_Lamp(state, world)


def MM_DoubleDoor(state, world):
    return MM_UFODoor(state, world) and HasHoop(state, world) and HasRC(state, world)


def MM_SpaceMonkeys(state, world):
    return MM_DoubleDoor(state, world) and HasFlyer(state, world)


def MM_FinalBoss(state, world):
    return (MM_DoubleDoor(state, world) and HasSling(state, world) and HasFlyer(state, world)) or (
                MM_UFODoor(state, world) and SuperFlyer(state, world))


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
