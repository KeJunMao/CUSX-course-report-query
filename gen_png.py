from cairosvg import svg2png
from User import User
from ranking import get_rank_info


def gen_item(name, value, index):
    if value >= 90:
        color = "#81c784"
    elif value >= 80:
        color = "#03a9f4"
    elif value >= 60:
        color = "#ff9800"
    else:
        color = "#f44336"
    return f"""<g transform="translate(0, {index*40})">
        <text data-testid="lang-name" x="2" y="15" class="lang-name">{name}</text>
        <text x="215" y="34" class="lang-name">{value:.2f}</text>
        <svg width="205" x="0" y="25">
          <rect rx="5" ry="5" x="0" y="0" width="205" height="8" fill="#ddd" />
          <rect height="8" fill="{color}" rx="5" ry="5" x="0" y="0" data-testid="lang-progress" width="{value}%">
          </rect>
        </svg>
      </g>"""


def gen_title(title):
    return f"""<g data-testid="card-title" transform="translate(25, 35)">
    <g transform="translate(0, 0)">
      <text x="0" y="0" class="header" data-testid="header">{title}</text>
    </g></g>"""


def gen_subtitle(title):
    return f"""<g xmlns="http://www.w3.org/2000/svg" data-testid="card-subtitle" transform="translate(25, 55)">
    <g transform="translate(0, 0)">
      <text x="" y="0" class="subtitle" data-testid="subtitle">{title}</text>
    </g></g>
  """


def gen_svg(title, subtitle, course):
    svg_title = gen_title(title)
    svg_subtitle = gen_subtitle(subtitle)
    svg_style = """<style>
    *{
      font-family: 'Heiti SC Medium'
    }
    .header {
      font: 600 18px 'Heiti SC Medium';
      fill: #2f80ed;
    }
    .subtitle {
      font: 400 13px 'Heiti SC Medium';
      fill: #2f80ed;
    }
    .lang-name {
      font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #333
    }
  </style>"""
    items = []
    for i, s in enumerate(course):
        items.append(gen_item(name=s['名称'], value=s['成绩'], index=i))
    height = 85+(len(items)+1)*40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="{height}" viewBox="0 0 300 {height}" fill="none">
  {svg_style}
  <rect data-testid="card-bg" x="0.5" y="0.5" rx="4.5" height="{height-1}" stroke="#e4e2e2" width="299" fill="#fffefe"
    stroke-opacity="1" />
  {svg_title}
  {svg_subtitle}
  <g data-testid="main-card-body" transform="translate(0, 65)">
    <svg data-testid="lang-items" x="25">
      {' '.join(items)}
      <g transform="translate(0, {(len(items))*40})">
        <text data-testid="lang-name" x="2" y="20" class="lang-name">感谢微信扫码支持我的公众号</text>
        <text data-testid="lang-name" x="2" y="35" class="lang-name">扫这个码，你容易，我不容易</text>
        <image href="./qrcode.jpg" x="215" y="10" height="30" width="30"></image>
      </g>
    </svg>
  </g>
</svg>"""


def gen_png(user: User, course):
    total = user.getTotal(course)
    rank_info = get_rank_info(user.username)
    subtitle = f"总分:{total:.2f} 均分:{total / len(course) if len(course) > 0 else 1:.2f} 排名:{rank_info['ranking']:.0f}/{rank_info['total_users']}"
    svg_code = gen_svg(title=user.username, subtitle=subtitle, course=course)
    return svg2png(bytestring=svg_code, output_width=800)
