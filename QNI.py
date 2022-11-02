# Quantifier Negation sentence Identifier
import spacy
spacy.prefer_gpu()
import en_core_web_sm
nlp = en_core_web_sm.load()
print('INFO: spaCy initialized successfully.')


def get_quantifier(sentence, quantifiers: list[str]):
    doc = nlp(sentence)
    dep = ['det', 'poss', 'advmod', 'nmod', 'nsubj', 'nsubjpass', 'ROOT']

    for token in doc:
        if (token.text.lower() in quantifiers) and (token.dep_ in dep):
            if token.text != 'know':
                return token

    return None


def assoc_negation_exists(sentence, q_root):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'neg':
            if (token.head.text == q_root.text and token.head.i == q_root.i) or (
                    token.head.head.text == q_root.text and token.head.head.i == q_root.i):
                return True
    return False


def get_q_root(quantifier):
    case_1 = ['nsubj', 'nsubjpass']
    case_2 = ['det', 'poss', 'advmod', 'nmod']
    dep = quantifier.dep_

    q_head = quantifier.head
    if dep in case_1:
        if q_head.dep_ == 'nsubj' or q_head.dep_ == 'auxpass':
            return q_head.head
        else:
            return q_head
    elif dep in case_2:
        return q_head.head


def reversed_traversal(sentence, quantifiers):
    doc = nlp(sentence)
    negation = None
    for token in doc:
        if token.dep_ == 'neg' or token.dep_ == 'preconj':
            negation = token
    if negation == None:
        return False

    ancestor = negation
    while ancestor != ancestor.head:
        ancestor = ancestor.head

    for quantifier in quantifiers:

        if ancestor.dep_ == 'ROOT' and quantifier in ancestor.text:
            return True
        for token in doc:
            if token.head == ancestor and quantifier in token.text and token.i < ancestor.i:
                return True

    return False


def is_quantifier_negation(sentence: str, quantifiers):
    quantifier = get_quantifier(sentence, quantifiers)
    if quantifier is None:
        return False

    "Second check"
    if reversed_traversal(sentence, quantifiers):
        return True

    q_root = get_q_root(quantifier)
    if assoc_negation_exists(sentence, q_root):
        return True

    return False

def validate_quant_neg(transcript: list[str], quantifiers):
    for sentence in transcript:
        if is_quantifier_negation(sentence, quantifiers):
            return True

    return False

def is_standalone():
    pass

def find_quantifier_negation(sentences, quantifiers):
    print('INFO: Beginning search for quantifier + negation statements.')
    quants = []
    sents = []
    standalone = []
    i = 0
    indices = []
    for sentence in sentences:
        if is_quantifier_negation(sentence, quantifiers):
            quants.append(get_quantifier(sentence, quantifiers).text)
            sents.append(sentence)
            indices.append(i)
            # standalone.append("True" if is_standalone(sentence, quantifiers) else "False")

        i = i+1

    print('INFO: Search completed with ' + str(len(sents)) + ' potential quantifier + negations.')
    print("\n")
    return quants, sents, indices

def get_context(sentences, indices):
    ret = []
    for index in indices:
        start = index - 3
        end = index + 2
        if start <= 0:
            start = 0
        elif end > len(sentences):
            end = len(sentences)
        for i in range(start, end):
            ret.append(sentences[i])
        ret.append('**********')
    return ret

if __name__ == '__main__':
    sentences = ['MICHEL MARTIN, host: ', "I'm Michel Martin, and this is TELL ME MORE from NPR News. It's time for our weekly shape-up at the Barbershop, where the guys talk about the news and whatever's on their minds. Sitting in the chair for a cut this week are freelance writer Jimi Izrael, civil-rights attorney and editor Arsalan Iftikhar, media executive Nick Charles and syndicated columnist Ruben Navarrette. Hey Jimi, what's up? ", "Mr. JIMI IZRAEL (Freelance Writer): Hey, hey yo, what's up fellas? Welcome to the shop. How are we doing? ", "Mr. RUBEN NAVARRETTE (Syndicated Columnist): Hey, J., what's happening, man? ", 'Mr. NICK CHARLES (Media Executive): (Unintelligible) pretty good. ', "Mr. IZRAEL: Yo, what's up, man? John McCain and Barack Obama showed and proved in the Potomac, with Obama rockin' Hillary (unintelligible) something fierce, man. What happened? And you know what? What's interesting is Mitt Romney's come out to endorse McCain, man. Ruben, what's up with that? ", "Mr. NAVARRETTE: What is up with that? And it's getting really interesting on the presidential race. I personally don't think Romney's endorsement of McCain is going to do a lot of good because the anti-McCain vitriol on the right wing is just so strong that if anything, now those folks are likely to turn against Romney. They're not likely to re-think their thoughts about McCain. ", "Now on the Democratic side, it's getting even better because every single time that Hillary gets a beat-down, and she's gotten eight straight beat-downs in a row, and eight primaries or caucuses have gone to Obama - every time this happens, the Clinton camp brings out the long knives and the bad rhetoric, and they've been saying and doing all this vicious stuff about Obama. ", "Most recently, Ed Rendell, the governor up in Pennsylvania and a Hillary Clinton backer, floated the idea that white folks won't vote for a black guy, and I just think this is nuts. This is the stuff the Democrats said the Republicans used to do, and now Democrats are doing it. ", 'Mr. IZRAEL: Nick, what do you think about that? ', "Mr. CHARLES: Well, you know, my thing about it is that in terms of Republicans, this is John McCain's gold watch. He's not going to win the presidency in November, so this is his gold watch for all the years of service, going to the Hanoi hotel, Hanoi Hilton, and he gets a gold watch - he's going to get the nomination whether or not conservatives are on board, whether or not Ann Coulter likes it, he's going to get it. I don't think he has a chance in November, either against Hillary or Obama. ", "On the Democratic side, I agree with Ruben, you know. I'm waiting for somebody to come out with N-word in any minute now. It's getting really vicious. You can see it in her stump speeches in Wisconsin. You can hear it in the subtle rhetoric of Bill Clinton that they're thoroughly discombobulated, thoroughly upset and caught off-guard. ", 'They really thought this was going to be a coronation, and now not only has he tied, he has surpassed her, and the long knives are turning into cleavers, and these folks are just going to start hacking. ', 'MARTIN: I wanted to ask Ruben a question, though, about the - one of the sort of signs that a campaign is in trouble is when they start firing people, and the Clinton campaign - well, fired is maybe not the right word. Patti Solis Doyle, who was the campaign manager, the first Latina to run a national campaign, was replaced by Maggie Williams, and Ruben, I was just wondering: is this the kind of thing that people care about? Does anybody care about it, or is that just inside baseball? ', "Mr. NAVARRETTE: Latinos care about it. It's inside baseball for a lot of other folks, but Latinos care about it as follows. If you had had an African-American in a high-profile position, and the campaign had gone around and said that, you know, made a big deal out of that, and then one day you woke up and that person was gone, the response would be okay, listen, you don't get any gold star for that. You don't get any diversity credit for that because that person's not there anymore. ", "And a lot of Latinos up on the East Coast in particular are raising questions about what happened to Patti Solis Doyle, and here's why: because she goes way back with Hillary Clinton, but anybody can see that Patti Solis Doyle didn't blow those elections. Those elections were blown by Hillary Clinton and Bill Clinton. They don't need a campaign manager; they need a new candidate. ", '(Soundbite of laughter) ', "MARTIN: Well, I don't know, though. Don't they have a right to have people run their campaign as they see fit? If you're not getting the results, somebody's got to take the fall. It's like firing the manager of a baseball team. The manager's got to go. That's the way it is. ", "Mr. NAVARRETTE: I agree with that, but a lot of Latinos disagree with me, and they think that this is kind of a typical Clinton MO, use people and discard them when they're no longer useful. ", "Mr. ARSALAN IFTIKHAR (Civil-rights Attorney and Editor): Well, and for Democrats especially - I think for us what is most telling is if you look at both Hillary and Barack's acceptance speeches around the primaries and look at the audience behind them, behind Hillary is the old, white, establishment Democratic Party. Behind Barack is the new rainbow coalition, if you will, of this new generation, this new sort of youth, progressive, grass-roots movement that is black, that is white, that is Christian, that is Muslim, that is Jewish, that is straight, that is - that represents all of America, and I think that, you know, for many Democrats, they're really waking up to the fact that Hillary is just part of the establishment, and she's just part of the political machine. ", "MARTIN: I do have to remind people that Arsalan's an Obama supporter. I just have to make sure everybody knows, in case, you know, it wasn't really clear from what you just said. Go ahead, Nick. ", "Mr. CHARLES: I think what you have to be careful of is not to count her out yet. You know, she's on the mat at the count of six. She has four more counts to get up off the mat. And the thing about it, they're willing to rend the relationship that black folks have had with the Democratic Party with half a century to win this election by saying that there's a division between Latinos and blacks, now trying to pit Latinos against blacks. They're willing to do that to win this election. So God knows what they're willing to do between now and then. ", "You know, I'm not supporting either one ostensibly, but the tactics of the Clintons are very, very brazen and are going to get even more brazen as you get closer and closer to Texas, Ohio, and I don't even think Pennsylvania because Texas and Ohio is - it's going to be firewall. ", 'MARTIN: I just want to point out, just in the spirit of fairness, that there are some people who think that the Obama people are meaner than the Clinton people in that… ', "Well I know - just in that - they're saying you find more Obama people saying if she's the nominee, I'm not voting for her because I'm not digging the way they ran this campaign. ", "Mr. NAVARRETTE: Well, it's hold your nose and go to the booth, like many conservatives are going to do with John McCain. You know, we sort of view Hillary in that same regard also that obviously, we want to see a change in administration, but we might hold our nose while going to ballot box, also. ", 'MARTIN: Just one other thing I was wondering if I could run past you is there was this really interesting debate over the super-delegates. ', "Nick, you were saying taking it down to the wire and counting every vote. Well, this is an issue that is clearly going to go down to the wire, and the question then becomes what to do about the delegates from Michigan and Florida, who are not supposed to be counted because the party decided that since they moved their primaries up that the delegates shouldn't be seated - sorry, that's not a super-delegate question, it's a delegate question as well as a super-delegate question - and you had this interesting split in the civil-rights community over this. ", "I mean, Julian Bond(ph) on the one hand saying this is another example of voters being disenfranchised, many of them minority voters, and then Al Sharpton saying, you know, the rules are the rules. You know, there are a lot of people who probably didn't vote because they didn't think their votes would count so their votes are not being reflected, so it's not fair - I just was curious what folks think about that. ", "Mr. CHARLES: That's (Unintelligible). ", 'Mr. NAVARRETTE: Since when does Al Sharpton want to play by the rules? ', '(Soundbite of laughter) ', 'Mr. CHARLES: Well, the funny thing is - you know something, this is one of the few times that I agree with Al Sharpton, that and my love of James Brown - is that, you know, this reminded me of the movie "The Man" with James Earl Jones as the president. You know, he gets in there by accident, and Martin Boylson(ph) says to him when he\'s running, you know, you got through the back door. These folks are trying to come through the plumbing. And the fact of the matter is this is what they\'re trying to do. ', "Mr. NAVARRETTE: That's true. ", "Mr. CHARLES: Everybody had an opportunity in October to say these folks do not count. Everybody agreed they don't count. ", 'Mr. NAVARRETTE: Right. ', 'Mr. IFTIKHAR Right. ', "Mr. CHARLES: Now all of a sudden you're behind by delegates, they should count, and a phone call from Bill Clinton to Julian Bond under the cover of civil rights is - this is what it is. Let's call it what it what is. Let's call it what it is. ", "Mr. NAVARRETTE: Well, the super-delegates thing, just very quickly because Michel mentioned that, that feeds into this notion that a lot of people have that the Hillary camp will do anything, that nothing is beneath the Clinton. Okay, they will stoop as low as they need to stoop to steal this election from Barack Obama. For people who believe that narrative, they think super-delegates are the way that Hillary steals the election. I don't think so. ", "MARTIN: If you're just joining us, I'm Michel Martin, and you're listening to Ruben Navarrette, Nick Charles, Arsalan Iftikhar and Jimi Izrael in the Barbershop. ", "Mr. IZRAEL: Speaking of sneaky tactics, your boy, pitcher Roger Clemens and former trainer Brain McNamee answered in front of Congress this week to allegations of steroid use. Nick, Clemens was up there head-to-head with McNamee. I'll tell you what, neither one of them read credible to me. Who's lying? ", 'MARTIN: Hold on a second. Before - for folks who missed the hearings, you want to just hear a little bit of what they said? ', '(Soundbite of Congressional Committee Hearing) ', 'Mr. ROGER CLEMENS (Pitcher): Let me be clear. I have never taken steroids or HGH. ', 'MARTIN: And then this is Brian McNamee… ', '(Soundbite of laughter) ', 'MARTIN: Okay, well that was Roger Clemens. ', 'Mr. NAVARRETTE: It was short and sweet. ', "MARTIN: And here's Brian McNamee, who's his former trainer, who also testified at the same hearing sitting a couple of seats away, not making eye contact. ", 'Mr. BRIAN McNAMEE (Former Trainer of Mr. Roger Clemens): I have no reason to lie and every reason not to. If I do lie, I will be prosecuted. I was never promised any special treatment or consideration for fingering star players. I was never coerced to provide information against anyone. All that I was ever told to do was to tell the truth to the best of my ability, and that is what I have done. ', 'I told the investigators that injected three people, two of whom I know confirmed my account. The third is sitting at this table. ', "MARTIN: I know, it's sad. ", "Mr. CHARLES: I (unintelligible) yesterday, and my thing is this. I'm a representative of Eliza Cummings of Maryland. Any Pettitte is the person I believe, and if Andy Pettitte, who was not there yesterday, has a deposition that says Roger Clemens said to him that I use HGH, and Roger Clemens is saying that Andy Pettitte is a stand-up guy, then he's saying a guy who's a stand-up guy - now you're saying he misremembered? The sad fact is whatever he used or didn't use, in the court public opinion, people don't believe him, and he's trying to salvage a reputation and a Hall of Fame nomination, and the happiest person right now in America is Barry Bonds because he's out of the show. ", 'Mr. NAVARRETTE: Barry Bonds, absolutely. ', "Mr. IZRAEL: But you know what, Nick? You know what? You make that point, but McNamee, I mean he's not exactly the most credible cat in the crew, man, I mean he's on record lying, too, and deceiving in some of his testimony, so I don't know, man. To me it's kind of like neither one of them have any real motivation to tell the truth. ", "Mr. CHARLES: That's what I'm saying. The both of them, if he's a rat and a snitch, and Clemens is trying to protect that image, that's why it's a wash. That's why I believe Pettitte, and more importantly, if he admits that this guy was up in his bedroom with his wife getting injected, what else wouldn't he do? You know, he doesn't deny that, you know, McNamee injected his wife, and he said I didn't know. Come on, you're going to tell me your wife is going to have some guy up in the room injecting her with some foreign substance, and you don't know? ", 'Mr. NAVARRETTE: Right. ', '(Soundbite of laughter) ', 'Mr. IZRAEL: That whole scenario is just jacked up. ', "Mr. CHARLES: You know, it's kind of whack right there. ", 'Mr. IZRAEL: Yo, A-Train. ', "Mr. IFTIKHAR: Well, yeah, and I agree with Nick completely, and let's remember this is a Congressional hearing here, and so basically these guys have so much invested - they basically have to stick with whatever story they're said from the beginning. ", 'Mr. IZRAEL: Oh yeah. ', "Mr. IFTIKHAR: And so I mean, you know, at the end of the day I think that McNamee had a lot more to lose. He had nothing to gain by lying. I think Clemens just basically, you know, is towing his party line that he's done from the beginning, and he's going to be asterisked like Barry Bonds for the rest of his career. ", "Mr. NAVARRETTE: There's a way out of this mess. I was trying to figure out all week, how could it be that both these guys are telling the truth, and now I figured it out. In an ode to Bill Clinton, it all depends on the meaning of the word steroid. ", '(Soundbite of laughter) ', '(Soundbite of groaning) ', "MARTIN: That's sad, though, isn't it, though? I've got to tell you, it's sad. I just - I just hate watching this stuff. I hate having these guys up there… ", "Mr. IFTIKHAR: Why do you think it's sad, Michel? ", "MARTIN: I think it's that people invest so much in careers in athletics, they give up so much, they start - they gain a lot when they get to the pros, but they start at such a young age - they shut out pretty much everything else but athletics to build to that point, and then you see it slipping away. I'm not justifying it, but you know, you see the age at which, you know, these kids start, you know, doing the sports. They get coaching, you know, when they're six years old and, you know, whatever, and it just seems like we invest so much in sports, and then we build these people up, and then they screw up, and we bring them down, and that's all I have to say about it. ", "Mr. CHARLES: The second part of what you said is right. That's the problem. We invest too much in these people. ", "MARTIN: And they have every reason to protect it because who wants to get off that mountaintop? Who wants to move from first class into coach? You know, who wants to be the one to have to actually stand in line to go to the best restaurant. They want to be able to just walk right through the door. And to give all that up and, you know, sure, you know, we've got folks out there, you know, in Iraq and Afghanistan laying their lives on the line. That's a really big deal, and in contrast this isn't, but it just - you see these guys, many of them who are not, you know, affluent, and everything they have comes from sports. You can see why they don't want to give it up, guys and women. That's all I wanted to say. ", "Mr. NAVARRETTE: And also, when you had Congressman Keith Ellison on a few weeks ago, he said that, you know, my kids are athletes, and what sort of message is this sending to the kids of America in terms of, you know, people who have these athletic aspirations as to, you know, what is okay and what isn't okay to do. ", 'And so for that in terms of our sort of societal discourse, I think that, you know, it did play a public service. ', "Mr. IZRAEL: In more-serious news - now this is serious, bro - I guess Beyonce started a cat fight by not giving Aretha Franklin, the Queen of Soul, her props. And there's probably no quicker way, without taking away plate, to get her angry. Yo. ", '(Soundbite of laughter) ', "MARTIN: You guys, I don't know if everybody saw the moment because, you know, everybody wasn't watching, but just in case, here's a little longer performance - here, we'll just play it. ", '(Soundbite of Grammy Award Presentation) ', '(Soundbite of music) ', 'Ms. BEYONCE (Singer): But there is one legend who has the essence of all of these things: the glamour, the soul, the passion, the strength, the talent. Ladies and gentlemen, stand on your feet and give it up for the queen. ', '(Soundbite of applause) ', "MARTIN: She's talking about Tina Turner. That's what's up with that. ", "Mr. CHARLES: That is just - you know, it probably - Beyonce could probably run away from Aretha, but if Aretha catches her with a headlock, it'll take all of Jay-Z's posse to pry her loose. ", "Mr. IZRAEL: It's a real mess. She could put mustard on a bun and put Beyonce in it and eat her for lunch. ", 'Mr. NAVARRETTE: You have to give Aretha some respect, ba-dum-dum. ', '(Soundbite of laughter) ', "Mr. IFTIKHAR: But isn't this kind of divas being divas here? I mean, you know, at the end of the day I think a compelling argument could be made for Tina Turner. I mean… ", 'Mr. IZRAEL: Oh no, come on now. ', "Mr. NAVARRETTE: Actually he's right. He's right. ", "Mr. IFTIKHAR: No he's not. No he's not. ", 'Mr. NAVARRETTE: Compelling argument. ', 'Mr. IZRAEL: A-Train, make that argument. ', 'Mr. IFTIKHAR: "What\'s Love Got to Do with It?" That\'s all - I mean. I mean, you know, Aretha is old-school. Tina, you know, helped redefine the 80s in my opinion. ', "Mr. IZRAEL: Well actually, I was thinking a little more along the lines that, you know, Tina Turner with Ike Turner, she was one of the architects of what we understand to be rock and roll. For a long time, she was called the Queen of Rock and Roll. And not just that, it could've been kind of - not a slip slip but kind of a weird slip because you guys know that in Pink Floyd - was it Pink Floyd or was it - oh no, it was The Who's play, I think. She placed the African queen. So I mean, it could've been some kind of allusion to that. But as far as her stuff in the 80s, I don't know if Tina did anything of note, you know, beyond, you know beyond Thunderdome, you know, to qualify as queen of much, you know. But I mean, Aretha's undisputed. ", "I think what needs to happen here is maybe there needs to be like a diva battle, like Tina Turner, you know, Aretha Franklin and Beyonce, and you know, Aretha needs to blow them both off the stage and show them why she gets R-E-S-P-E-C-T. That's what's up. I'm that dude. ", '(Soundbite of laughter) ', "Mr. IZRAEL: And I certainly approve that message. It's a wrap. Gentlemen, thank you so much for coming to the shop, and I have to kick it back to the lady of the house. ", "MARTIN: That's right. Who's the queen up in here? ", "MARTIN: That's what I'm talkin' about. Ruben Navarrette writes for the San Diego Union Tribune and cnn.com. He joined us from his office in San Diego. Arsalan Iftikhar is a contributing editor for Islamica Magazine and a civil-rights attorney. He joined us from our studios here in Washington. Nick Charles is a vice president of digital content at bet.com. He joined us from our bureau in New York. Jimi Izrael is a freelance writer and a blogger for theroot.com. He joined us from WSSU in Tallahassee, Florida. You can find links to all of our Barbershop guests at our Web site, npr.org/tellmemore. Gentlemen, thanks so much for joining us. ", 'Mr. CHARLES: Thank you, Michel. ', 'Mr. IZRAEL: Yup, yup. ', "MARTIN: I think I should mention that a couple of us mispronounced the name of Roger Clemens' trainer. It's Brian McNamee. Sorry for that error. ", 'NPR transcripts are created on a rush deadline by an NPR contractor. This text may not be in its final form and may be updated or revised in the future. Accuracy and availability may vary. The authoritative record of NPR’s programming is the audio record.']
    print(find_quantifier_negation(sentences, ['every', 'some', 'no']))
