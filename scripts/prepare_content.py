"""Build the static teaching materials from reviewed lesson content."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def write(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
segments = [
 ('简便计算', 30, 30), ('因式分解的方向', 40, 50), ('公因式', 40, 50),
 ('提取与检验', 60, 75), ('商式中的1', 40, 50), ('当堂检测', 50, 30),
 ('课堂归纳', 20, 20),
]

# 每项是一个投影文字行。位置和字重由 render_slide_images.py 控制。
visible = [
 [('head','简便计算'),('formula','25×7＋25×3'),('body','怎样计算更简便？')],
 [('formula','25×7＋25×3＝25×(7＋3)＝250'),('body','共同的 25 被提到括号外')],
 [('formula','a(b＋c)＝ab＋ac'),('body','展开：整式的积 → 多项式'),('body','右边能否重新写成积？')],
 [('formula','ab＋ac＝a(b＋c)'),('body','多项式 → 几个整式的积'),('key','因式分解（分解因式）')],
 [('formula','6x²＋9x'),('body','6 与 9 共有怎样的数因数？'),('body','x² 与 x 共有怎样的字母因式？')],
 [('head','公因式：3x'),('formula','6x²＝3x·2x'),('formula','9x＝3x·3')],
 [('formula','6x²＋9x'),('formula','＝3x·2x＋3x·3'),('body','共同提出 3x，括号内留下什么？')],
 [('formula','6x²＋9x＝3x(2x＋3)'),('check','检验：3x(2x＋3)＝6x²＋9x')],
 [('warning','待判断的解法'),('formula','3x²＋3x＝3x·x'),('body','右边展开能还原左边吗？')],
 [('formula','3x＝3x·1'),('result','正确：3x²＋3x＝3x(x＋1)'),('body','当某项恰好等于公因式时，商为 1。')],
 [('head','当堂检测'),('result','分解因式：8a²－12a'),('body','请先找公因式，再写积并检验。')],
 [('formula','8a²－12a＝4a(2a－3)'),('check','检验：4a(2a－3)＝8a²－12a')],
 [('question','回顾：提公因式法怎样做？'),('body','如何检查结果没有漏项？')],
 [('process','找公因式 → 各项相除写成积 → 乘回检验'),('body','易错提醒：某项等于公因式，除后为 1。')],
 [('head','课后作业｜巩固练习（选做）'),('result','分解因式：10m²n－15mn²'),('body','要求：① 找出公因式；② 写成整式的积；③ 展开检验。')],
]
homework = '课后选做这道题，先找公因式，再写成积，最后用展开进行检验。今天的学习就到这里。'

def timestamp(seconds):
 return f'{seconds//60:02d}:{seconds%60:02d}'

pages = []
script = ['# L01 十分钟无生试讲逐字稿\n\n教材参照：淮北市现行沪科版七年级下册8.4。所有学生回答均为预设。计时包含板书、停顿与翻页。设计预算600秒，实际用时待排练。\n']
for i, (title, first, second) in enumerate(segments, 1):
 for state, seconds in zip('AB', (first, second), strict=True):
  pages.append(dict(page_id=f'L01-S{i:02d}{state}', title=title, seconds=seconds, segment=i))

# Align the spoken reveal with these specific display states.
reveal_notes = {
 'L01-S01A': '同学们，请看这道计算题：25乘7加25乘3。想一想，怎样算更简便？【停顿5秒】观察两项中有没有相同的数。',
 'L01-S01B': '两项中都有25。用乘法分配律，可以先把7和3相加，再乘25，得到250。我们把共同的25提到括号外。接下来，把这样的想法用到含字母的式子中。',
 'L01-S02A': '我们已经会用乘法分配律展开：a乘括号b加c，得到ab加ac。这是由积写成和。现在请反过来看：能把右边重新写成积吗？【停顿5秒】',
 'L01-S02B': 'ab加ac的每一项都有因式a，可以写成a乘括号b加c。把一个多项式化成几个整式的积，叫作因式分解，也叫分解因式。【左栏板书】展开是由积到和，因式分解是由多项式写成积。今天我们学习提公因式法。',
 'L01-S03A': '请看6x的平方加9x。先观察系数6和9，它们的最大公因数是多少？再比较x的平方和x，共同的字母部分是什么？【停顿】',
 'L01-S03B': '【预设：最大公因数是3，共同的字母部分是x】相同字母取最低次数，所以本例提出3x。6x的平方等于3x乘2x，9x等于3x乘3。【中栏板书并停顿】本节练习按整系数多项式组织。',
 'L01-S04A': '把两项拆开看。6x的平方除以3x，商是2x；9x除以3x，商是3。【板书拆写过程】两项之间是加号。共同提出3x，括号里留下什么？【停顿5秒】',
 'L01-S04B': '【预设：2x加3】得到3x乘括号2x加3。【完成板书】用分配律乘回去，3x乘2x得到6x的平方，3x乘3得到9x，正好还原原式。括号内的每一项都对应原式的一项。【停顿，指板书复述】',
 'L01-S05A': '请看一个待判断的解法。3x的平方加3x，被写成了3x乘x。右边展开能还原左边吗？【停顿5秒】你能指出少了哪一项吗？',
 'L01-S05B': '右边展开只有3x的平方，少了3x。第二项3x等于3x乘1，提出3x以后，括号里对应的是1。正确结果是3x乘括号x加1。【板书并圈出1，再乘回核对】',
 'L01-S06A': '请独立分解8a的平方减12a。先找公因式，再写成积并展开检验。【独立思考与书写约20秒】',
 'L01-S06B': '公因式是4a。两项分别除以4a，得到2a和负3。写成4a乘括号2a减3，乘回去恰好还原原式。【右栏板书结果】',
 'L01-S07A': '【指向黑板中栏】提公因式法怎样做？最后怎么检查没有漏项？【停顿】',
 'L01-S07B': '先找公因式，再逐项相除写成积，最后乘回检验。某项等于公因式时，商是1，要留在括号里。【完成底栏板书】',
}
pages.append(dict(page_id='L01-S08A',title='课后作业',seconds=15,script=homework,
                  teacher_only='E06 备课答案：5mn(2m－3n)。',segment=8))
elapsed = 0
for page, lines in zip(pages, visible, strict=True):
 page['layout'] = lines
 page['text'] = [line for _, line in lines]
 if 'script' not in page:
  page['script'] = reveal_notes[page['page_id']]
 page['start_seconds'] = elapsed
 page['prompt_path'] = f"slides/prompts/{page['page_id']}-v2.md"
 write(page['prompt_path'], '制作一张 1920×1080 的七年级数学投影幻灯片。背景 #F8FAFC，正文深蓝，青绿强调，待判断内容用琥珀色标示。中文黑体，公式用数学衬线字体，左右留白 8%。题头靠左，公式居中或逐行对齐，提问与说明在下方。完整保留下面每行文字及数学符号。\n\n'+'\n'.join(page['text'])+'\n')
 elapsed += page['seconds']
assert elapsed == 600
for page in pages:
 start=page['start_seconds']; end=start+page['seconds']
 script.append(f"## {timestamp(start)}—{timestamp(end)} {page['page_id']} {page['title']}\n\n{page['script']}\n")
write('slides/pages.json',json.dumps(pages,ensure_ascii=False,indent=2))
write('lesson-plans/L01-script.md','\n'.join(script))
plan='''# L01 教学设计：因式分解——提公因式法入门

## 基本信息

用途：师范生教学方法课程作业。形式：无生试讲。时长：10分钟。教材参照：淮北市现行沪科版《数学》七年级下册，根据2022年版课标修订，8.4节，第80—82页的概念与提公因式法基础。本设计是教材内容的十分钟重组。

## 教材与学情分析

教材在整式乘法之后系统引入因式分解，利用互逆变形建立联系，再学习提公因式法与公式法。本片段聚焦第一种方法。假设学生已学单项式乘多项式、乘法分配律及幂的运算；实际学情尚未调查。

## 教学目标与评价

1. 能指出ab＋ac到a(b＋c)是由多项式写成整式的积，以E02口头判断评价。
2. 能找出6x²＋9x的公因式3x，说明系数与字母依据，以E03追问评价。
3. 能完成8a²－12a的分解并展开检验，以E05当堂检测评价。

重点：识别公因式，逐项确定商式。难点：保留商式中的1，并理解提取与展开的互逆关系。例题按整系数多项式组织。

## 教学过程与设计意图

|环节|秒数|师生活动（回答为预设）|设计意图|
|---|---:|---|---|
|导入E01|60|数值简算，观察共同的25|用熟悉运算建立迁移起点|
|概念E02|90|比较展开与逆向写积|突出变形方向和结果形式|
|识别E03|90|观察6、9及x的共同部分|把找公因式的依据说清|
|示范E03|135|逐项改写、提取、展开检验|建立可复核的解题过程|
|辨析E04|90|判断漏1错例，展开并纠正|用运算证据解释错误|
|检测E05|80|独立练习20秒，展示答案与检验|检测独立迁移与减号保留|
|归纳|40|复述步骤，在板书底栏归纳|形成方法与检验习惯|
|选做作业E06|15|展示题目与要求，保留终版板书|迁移到含两个字母的多项式|

合计600秒，已包含停顿、板书与翻页。板书按左概念、中例题、右辨析与检测、底归纳形成。教师在写完关键式后面向学生，避免边遮挡板书边讲解。

## 预设应对

无生试讲时提问后停顿，再用“我们可以发现”等衔接语继续。预设学生只找出x时，追问系数6和9的最大公因数；漏写1时，要求展开，定位未还原的项。时间偏紧时压缩重复复述，保留独立练习、检验和漏1解释。

## 作业与反思

课后备选E06：10m²n－15mn²＝5mn(2m－3n)。用展开检验。排练表记录实际时长、板书遮挡、提问停顿及修改建议；当前没有真实课堂观察数据。练习与完整答案见统一练习文件。
'''
write('lesson-plans/L01-lesson-plan.md',plan)
write('slides/L01-storyboard.md','# L01 纯图分镜\n\n15个图像状态共600秒，含独立选做作业。精确文案、类型与时间见 pages.json。教师提示独立于投影画面。\n\n'+'\n'.join(f"- {p['page_id']}｜{timestamp(p['start_seconds'])}—{timestamp(p['start_seconds']+p['seconds'])}｜{' / '.join(p['text'])}" for p in pages)+'\n')
write('planning/project-brief.md','# 制作约定\n\n淮北市现行沪科版七年级下册8.4概念与提公因式法基础，无生试讲600秒。交付逐字稿、板书、教案和15页纯图PPTX及HTML。课件用浅底、深蓝、青绿色，板书用深绿、白、黄。\n')
write('references/sources.md','''# 来源与读取状态

检索：bocha-web-search。核验日期：2026-11-17至18日（北京时间）。

1. 淮北市教育局，2026-07-28现行教材公告：https://hbjy.huaibei.gov.cn/xwzx/tzgg/58046496.html 。已读取公告及附件1，七年级数学列上海科技出版社。
2. 安徽省教育厅关于教材版本的答复：https://jyt.ah.gov.cn/content/article/40648206 。已读。地区存在版本差异，本项目具体采用淮北参照。
3. 上海科技出版社教材服务：https://www.sstp.cn/elementary5.html ，电子教材：https://jc.sstp.cn/jiaocai 。已核官方书单链接。
4. 国家平台现行七下教材元数据：https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/ad4e72e9-625e-4a51-8e7e-3f3839438070.json 。已读，题名明确根据2022年版课程标准修订，源PDF文件名ISBN9787547868836。
5. 官方教材目录与正文图像：https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets/ad4e72e9-625e-4a51-8e7e-3f3839438070.t/zh-CN/1772506700322/transcode/image/6.jpg 。已看目录及87—90.jpg（纸质80—83页），8.4起于80页，81页提公因式法，82页开始公式法。已看七上目录，无因式分解独立专题。“首次”指首次独立系统讲授，未作全书词频检索。
6. 教育部课标发布通知：https://www.moe.gov.cn/srcsite/A26/s8001/202204/t20220420_619921.html 。博查摘要已读；具体课标PDF条款与页码未核，本教案未引用未经核实的条款。

题目为本项目原创编排，教材仅供教学范围与结构参照；站点不附教材整册文件。
''')
print('Prepared',len(pages),'states;',sum(p['seconds'] for p in pages),'seconds')
