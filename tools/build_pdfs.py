from pathlib import Path
from html.parser import HTMLParser
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT=Path(__file__).resolve().parents[1]
FONT='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('SageUnicode',FONT,shapable=True))
pdfmetrics.registerFont(TTFont('SageBangla','/System/Library/Fonts/Supplemental/Bangla Sangam MN.ttc',subfontIndex=0,shapable=True))
pdfmetrics.registerFont(TTFont('SageDevanagari','/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc',subfontIndex=0,shapable=True))
NAVY=colors.HexColor('#163172'); SAGE=colors.HexColor('#788D64'); PALE=colors.HexColor('#E8EEE2'); INK=colors.HexColor('#26394A')

class Extractor(HTMLParser):
    def __init__(self): super().__init__(); self.stack=[]; self.items=[]; self.buf=''
    def handle_starttag(self,tag,attrs):
        if tag=='section' and dict(attrs).get('class')=='guide-chapter': self.items.append(('pagebreak',''))
        if tag in ('h1','h2','h3','p','li'): self.stack.append(tag); self.buf=''
    def handle_data(self,data):
        if self.stack: self.buf+=data
    def handle_endtag(self,tag):
        if self.stack and self.stack[-1]==tag:
            text=' '.join(self.buf.split())
            if text and not text.startswith(('© 2026','This practical resource','यह practical resource','ಈ practical resource')): self.items.append((tag,text))
            self.stack.pop(); self.buf=''

def extract(file):
    p=Extractor(); p.feed(Path(file).read_text(encoding='utf-8')); return p.items

styles=getSampleStyleSheet()
title=ParagraphStyle('Title',fontName='SageUnicode',fontSize=25,leading=32,textColor=NAVY,spaceAfter=15)
h2=ParagraphStyle('H2',fontName='SageUnicode',fontSize=15,leading=21,textColor=NAVY,spaceBefore=12,spaceAfter=7)
h3=ParagraphStyle('H3',fontName='SageUnicode',fontSize=12,leading=17,textColor=SAGE,spaceBefore=8,spaceAfter=4)
body=ParagraphStyle('Body',fontName='SageUnicode',fontSize=10.5,leading=16,textColor=INK,spaceAfter=8)
bullet=ParagraphStyle('Bullet',parent=body,leftIndent=14,firstLineIndent=-8,bulletIndent=0)
note=ParagraphStyle('Note',parent=body,backColor=PALE,borderColor=SAGE,borderWidth=1,borderPadding=9,spaceBefore=10,spaceAfter=10)

def footer(canvas,doc):
    canvas.saveState(); canvas.setFont(getattr(doc,'languageFont','SageUnicode'),8); canvas.setFillColor(colors.HexColor('#66737B'))
    canvas.drawString(18*mm,12*mm,'Sage & Seed · Practical guides for better connection')
    canvas.drawRightString(A4[0]-18*mm,12*mm,str(doc.page)); canvas.restoreState()

def make_pdf(outfile,display_title,language,files,card=False):
    out=ROOT/outfile; out.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=19*mm,title=display_title,author='Sage & Seed')
    font_name = 'SageBangla' if language == 'বাংলা' else ('SageDevanagari' if language in ('हिंदी','मराठी') else 'SageUnicode')
    doc.languageFont = font_name
    local_title=ParagraphStyle('LocalTitle',parent=title,fontName=font_name)
    local_h2=ParagraphStyle('LocalH2',parent=h2,fontName=font_name)
    local_h3=ParagraphStyle('LocalH3',parent=h3,fontName=font_name)
    local_body=ParagraphStyle('LocalBody',parent=body,fontName=font_name)
    local_bullet=ParagraphStyle('LocalBullet',parent=bullet,fontName=font_name)
    local_note=ParagraphStyle('LocalNote',parent=note,fontName=font_name)
    story=[Paragraph('SAGE &amp; SEED',local_h3),Paragraph(display_title,local_title),Paragraph(language,ParagraphStyle('Lang',parent=local_body,textColor=SAGE,fontSize=11)),Spacer(1,5*mm)]
    if 'young-adult-guide' in outfile or 'caregiver-guide' in outfile:
        mottos = {
            'Español':'La persona antes que el diagnóstico.<br/>La dignidad antes que el cumplimiento.<br/>La relación antes que la actividad.<br/>La participación antes que terminar.',
            '普通话':'诊断之前，先看见这个人。<br/>服从之前，先维护尊严。<br/>活动之前，先建立关系。<br/>完成之前，先重视参与。',
            'हिंदी':'निदान से पहले व्यक्ति।<br/>अनुपालन से पहले गरिमा।<br/>एक्टिविटी (activity) से पहले रिश्ता।<br/>पूरा करने से पहले जुड़ाव।',
            'বাংলা':'রোগ নির্ণয়ের আগে মানুষ।<br/>নিয়ম মানানোর আগে মর্যাদা।<br/>অ্যাক্টিভিটির (activity) আগে সম্পর্ক।<br/>শেষ করার আগে অংশগ্রহণ।',
            'मराठी':'निदानापूर्वी व्यक्ती।<br/>नियम पाळण्यापूर्वी सन्मान।<br/>अॅक्टिव्हिटीच्या (activity) आधी नाते।<br/>पूर्ण करण्यापूर्वी सहभाग।',
            'ಕನ್ನಡ':'ರೋಗನಿರ್ಣಯಕ್ಕಿಂತ ಮೊದಲು ವ್ಯಕ್ತಿ.<br/>ಅನುಸರಣೆಗೆ ಮೊದಲು ಘನತೆ.<br/>ಆಕ್ಟಿವಿಟಿಗಿಂತ (activity) ಮೊದಲು ಸಂಬಂಧ.<br/>ಪೂರ್ಣಗೊಳಿಸುವುದಕ್ಕಿಂತ ಮೊದಲು ಸಂಪರ್ಕ.',
        }
        motto = mottos.get(language, 'Person before diagnosis.<br/>Dignity before compliance.<br/>Relationship before activity.<br/>Engagement before completion.')
        story.extend([Spacer(1,18*mm),Paragraph(motto,local_note),PageBreak()])
    first=True
    for file in files:
        items=extract(ROOT/file)
        if not first and not card: story.append(PageBreak())
        first=False
        for tag,text in items:
            safe=text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            if tag=='h1': story.append(Paragraph(safe,local_h2))
            elif tag=='pagebreak': story.append(PageBreak())
            elif tag=='h2': story.append(Paragraph(safe,local_h2))
            elif tag=='h3': story.append(Paragraph(safe,local_h3))
            elif tag=='li': story.append(Paragraph('• '+safe,local_bullet))
            else: story.append(Paragraph(safe,local_body))
    if language=='Español':
        evidence='Nota sobre la evidencia: esta guía se basa en revisiones sistemáticas y síntesis de evidencia. La evidencia sobre habilidades de comunicación e interacción significativa es más consistente que la evidencia sobre resultados clínicos generales.'
        disclaimer='Este recurso práctico apoya la comunicación y la conexión. No es consejo médico, terapia, capacitación clínica ni certificación.'
    elif language=='普通话':
        evidence='证据说明：本指南参考系统综述与证据综合。关于沟通技巧和有意义互动的证据，比关于广泛临床结果的证据更一致。'
        disclaimer='本实用资源用于支持交流与联结，不属于医疗建议、治疗、临床培训或认证。'
    elif language=='বাংলা':
        evidence='প্রমাণ নোট (Evidence note): এই গাইড সাতটি সিস্টেম্যাটিক রিভিউ (systematic reviews) ও এভিডেন্স সিন্থেসিস (evidence syntheses) থেকে তৈরি। যোগাযোগের দক্ষতা ও অর্থপূর্ণ মিথস্ক্রিয়ার প্রমাণ বিস্তৃত ক্লিনিক্যাল ফলাফলের চেয়ে বেশি সামঞ্জস্যপূর্ণ।'
        disclaimer='এই ব্যবহারিক রিসোর্স (practical resource) যোগাযোগ ও সংযোগে সহায়তা করে। এটি মেডিক্যাল অ্যাডভাইস (medical advice), থেরাপি (therapy), ক্লিনিক্যাল ট্রেনিং (clinical training) বা সার্টিফিকেশন (certification) নয়।'
    elif language=='मराठी':
        evidence='पुरावा नोंद (Evidence note): ही मार्गदर्शिका सात सिस्टेमॅटिक रिव्ह्यूज (systematic reviews) आणि एव्हिडन्स सिंथेसिस (evidence syntheses) वर आधारित आहे. संवादकौशल्य आणि अर्थपूर्ण परस्परसंवादाचा पुरावा व्यापक क्लिनिकल परिणामांपेक्षा अधिक सुसंगत आहे.'
        disclaimer='हे प्रॅक्टिकल रिसोर्स (practical resource) संवाद आणि नाते जोडण्यासाठी आहे. हे मेडिकल अॅडव्हाइस (medical advice), थेरपी (therapy), क्लिनिकल ट्रेनिंग (clinical training) किंवा सर्टिफिकेशन (certification) नाही.'
    elif language=='हिंदी':
        evidence='एविडेंस नोट (Evidence note): यह गाइड सात सिस्टेमैटिक रिव्यू (systematic reviews) और एविडेंस सिंथेसिस (evidence syntheses) से जानकारी लेती है। कम्युनिकेशन स्किल्स (communication skills) और अर्थपूर्ण बातचीत का एविडेंस (evidence), व्यापक क्लिनिकल आउटकम्स (clinical outcomes) के एविडेंस से अधिक एकसमान है।'
        disclaimer='यह प्रैक्टिकल रिसोर्स (practical resource) बातचीत और जुड़ाव में सहायता के लिए है। यह मेडिकल एडवाइस (medical advice), थेरैपी (therapy), क्लिनिकल ट्रेनिंग (clinical training) या सर्टिफिकेशन (certification) नहीं है।'
    elif language=='ಕನ್ನಡ':
        evidence='ಎವಿಡೆನ್ಸ್ ನೋಟ್ (Evidence note): ಈ ಗೈಡ್ ಏಳು ಸಿಸ್ಟಮ್ಯಾಟಿಕ್ ರಿವ್ಯೂ (systematic reviews) ಮತ್ತು ಎವಿಡೆನ್ಸ್ ಸಿಂಥೆಸಿಸ್ (evidence syntheses) ಆಧರಿಸಿದೆ. ಕಮ್ಯುನಿಕೇಶನ್ ಸ್ಕಿಲ್ಸ್ (communication skills) ಮತ್ತು ಅರ್ಥಪೂರ್ಣ ಮಾತುಕತೆಗೆ ಇರುವ ಎವಿಡೆನ್ಸ್ (evidence), ವಿಶಾಲ ಕ್ಲಿನಿಕಲ್ ಔಟ್‌ಕಮ್ಸ್ (clinical outcomes) ಎವಿಡೆನ್ಸ್‌ಗಿಂತ ಹೆಚ್ಚು ಸ್ಥಿರವಾಗಿದೆ.'
        disclaimer='ಈ ಪ್ರಾಕ್ಟಿಕಲ್ ರಿಸೋರ್ಸ್ (practical resource) ಸಂಭಾಷಣೆ ಮತ್ತು ಸಂಪರ್ಕಕ್ಕೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ. ಇದು ಮೆಡಿಕಲ್ ಅಡ್ವೈಸ್ (medical advice), ಥೆರಪಿ (therapy), ಕ್ಲಿನಿಕಲ್ ಟ್ರೈನಿಂಗ್ (clinical training) ಅಥವಾ ಸರ್ಟಿಫಿಕೇಶನ್ (certification) ಅಲ್ಲ.'
    else:
        evidence='Evidence note: Informed by the seven systematic reviews and evidence syntheses listed at sageandseed.org/full-references.html. Evidence for communication skills and meaningful interaction is more consistent than evidence for broader clinical outcomes.'
        disclaimer='This practical resource supports communication and engagement. It is not medical advice, therapy, clinical training, or certification. Follow local safeguarding and supervisory procedures.'
    story.extend([Spacer(1,5*mm),Paragraph(evidence,local_note),Paragraph(disclaimer,local_body)])
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

langs={'en':('english','English'),'es':('spanish','Español'),'zh':('mandarin','普通话'),'hi':('hindi','हिंदी'),'bn':('bengali','বাংলা'),'mr':('marathi','मराठी'),'kn':('kannada','ಕನ್ನಡ')}
situation_slugs=['repeating-story','cannot-remember-name','cannot-find-word','seems-incorrect','no-answer','conversation-stops','seems-confused','frustrated','lose-interest','refuse-activity','seems-tired','emotional','cannot-understand','same-question','nothing-to-say']
activity_slugs=['family','music','sports','food','travel','gardening','art','objects','traditions','movies','work','school']
for code,(folder,label) in langs.items():
    titles={'en':('Young Adult Starter Guide','Caregiver Starter Guide','What Do I Do When...? Situation Guide Collection','Ways to Connect: Activity & Passion Guide','Young Adult Conversation Card','Caregiver Communication Card'),'es':('Guía inicial para jóvenes acompañantes de conversación','Guía inicial para cuidadores','¿Qué hago cuando...? Colección de situaciones','Formas de conectar: actividades e intereses','Tarjeta de conversación para jóvenes','Tarjeta de comunicación para cuidadores'),'zh':('青年交流伙伴入门指南','照护者入门指南','遇到这种情况怎么办？情境指南集','建立联结的方法：活动与兴趣','青年伙伴交流提示卡','照护者沟通提示卡'),'hi':('युवा साथी की शुरुआती गाइड','केयरगिवर की शुरुआती गाइड','ऐसा होने पर क्या करें?','बातचीत के तरीके','युवा साथी संवाद कार्ड','केयरगिवर कम्युनिकेशन कार्ड'),'bn':('তরুণ কথোপকথন-সঙ্গীর শুরুর গাইড','কেয়ারগিভারের শুরুর গাইড','এমন হলে কী করবেন?','সংযোগের উপায়','তরুণ সঙ্গীর কথোপকথন কার্ড','কেয়ারগিভার কমিউনিকেশন কার্ড'),'mr':('तरुण संवाद-साथीची सुरुवातीची मार्गदर्शिका','केअरगिव्हरसाठी सुरुवातीची मार्गदर्शिका','असे झाल्यास काय करावे?','संवाद जोडण्याचे मार्ग','तरुण साथीचे संवाद कार्ड','केअरगिव्हर कम्युनिकेशन कार्ड'),'kn':('ಯುವ ಸಂಗಾತಿಯ ಆರಂಭಿಕ ಗೈಡ್','ಕೇರ್‌ಗಿವರ್ ಆರಂಭಿಕ ಗೈಡ್','ಹೀಗೆ ಆದಾಗ ಏನು ಮಾಡಬೇಕು?','ಸಂಪರ್ಕದ ಮಾರ್ಗಗಳು','ಯುವ ಸಂಗಾತಿಯ ಸಂಭಾಷಣೆ ಕಾರ್ಡ್','ಕೇರ್‌ಗಿವರ್ ಕಮ್ಯುನಿಕೇಶನ್ ಕಾರ್ಡ್')}[code]
    make_pdf(f'assets/downloads/guides/{folder}/sage-seed-young-adult-guide-{code}.pdf',titles[0],label,[f'guides/{folder}/young-adult-starter.html'])
    make_pdf(f'assets/downloads/guides/{folder}/sage-seed-caregiver-guide-{code}.pdf',titles[1],label,[f'guides/{folder}/caregiver-starter.html'])
    make_pdf(f'assets/downloads/situation-guides/{folder}/sage-seed-situation-guides-{code}.pdf',titles[2],label,[f'situations/{folder}/{s}.html' for s in situation_slugs])
    make_pdf(f'assets/downloads/activities/{folder}/sage-seed-ways-to-connect-{code}.pdf',titles[3],label,[f'activities/{folder}/{s}.html' for s in activity_slugs])
    make_pdf(f'assets/downloads/cards/{folder}/sage-seed-young-adult-conversation-card-{code}.pdf',titles[4],label,[f'guides/{folder}/young-adult-card.html'],True)
    make_pdf(f'assets/downloads/cards/{folder}/sage-seed-caregiver-communication-card-{code}.pdf',titles[5],label,[f'guides/{folder}/caregiver-card.html'],True)
print('Created 42 PDFs')
