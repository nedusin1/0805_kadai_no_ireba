
from __future__ import annotations

from typing import Final

import streamlit as st


TITLE: Final = "※本当にあった　通信障害診断シミュレーター"


INVESTIGATIONS = {
    "A": {
        "title": "A　ほかのPCの通信状況を確認する",
        "targets": ["pc1", "router"],
        "result": "PC①と、2階以外にある別のPCは、どちらもインターネットに接続できました。",
        "meaning": "WAN側やホームルーター全体の障害である可能性は低いと考えられます。",
        "eliminates": ["WAN側", "ホームルーター全体"],
    },
    "B": {
        "title": "B　有線LANの接続と外観を確認する",
        "targets": ["cable_long", "cable_hubs", "cable_pc1", "cable_pc2"],
        "result": "すべての有線LANは端末に奥まで接続され、目立った折れや損傷もありませんでした。",
        "meaning": "単純なケーブル抜けや、目視で分かる大きな損傷の可能性は低くなります。",
        "eliminates": ["単純なケーブル抜け", "目視で分かる大きな損傷"],
    },
    "C": {
        "title": "C　ホームルーター・上流側ハブ・PC①間を確認する",
        "targets": ["router", "hub_upper", "pc1", "cable_long", "cable_pc1"],
        "result": "ホームルーター―上流側ハブ間と、上流側ハブ―PC①間ではリンクランプが点灯し、通信も正常です。",
        "meaning": "長い有線LANと、上流側ハブの基本的な中継機能は正常と考えられます。",
        "eliminates": ["長い有線LAN", "上流側ハブの基本機能"],
    },
    "D": {
        "title": "D　下流側ハブのリンクランプを確認する",
        "targets": ["hub_lower", "pc2", "cable_hubs", "cable_pc2"],
        "result": "上流側ハブとの接続ポートは点灯していますが、PC②との接続ポートは点灯していません。",
        "meaning": "上流側ハブ―下流側ハブ間ではリンクしていますが、下流側ハブ―PC②間では物理リンクが成立していません。",
        "eliminates": ["上流側ハブ―下流側ハブ間の完全な断線"],
    },
    "E": {
        "title": "E　下流側ハブの別ポートへ接続する",
        "targets": ["hub_lower", "pc2"],
        "result": "PC②につながるケーブルを下流側ハブの別ポートへ差し替えても、リンクランプは点灯しませんでした。",
        "meaning": "下流側ハブの特定の1ポートだけが故障している可能性は低くなります。",
        "eliminates": ["下流側ハブの特定ポート"],
    },
    "F": {
        "title": "F　2台のハブを交換する",
        "targets": ["hub_upper", "hub_lower"],
        "result": "2台のハブを交換しても、上流側と下流側のハブ間ではリンクし、下流側に置いたハブとPC②の間ではリンクしませんでした。",
        "meaning": "特定のハブ本体が原因である可能性は低くなります。",
        "eliminates": ["特定のハブ本体"],
    },
    "G": {
        "title": "G　PC①側とPC②側の有線LANを交換する",
        "targets": ["cable_pc1", "cable_pc2"],
        "result": "PC①で正常に使えていたケーブルをPC②側へ移しても、下流側ハブ―PC②間ではリンクしませんでした。",
        "meaning": "特定の末端ケーブルそのものが原因である可能性は低くなります。",
        "eliminates": ["特定の末端ケーブル"],
    },
    "H": {
        "title": "H　PC②を上流側ハブへ直接接続する",
        "targets": ["pc2", "hub_upper"],
        "result": "PC②を上流側ハブへ直接接続すると、インターネットに接続できました。",
        "meaning": "PC②のLANポートや基本的なネットワーク設定は正常と考えられます。",
        "eliminates": ["PC②本体", "PC②のLANポート", "PC②の基本設定"],
    },
}


DEVICE_LABELS = {
    "router": "ホームルーター",
    "hub_upper": "上流側ハブ",
    "hub_lower": "下流側ハブ",
    "pc1": "PC①",
    "pc2": "PC②（通信障害）",
    "cable_long": "長い有線LAN",
    "cable_hubs": "ハブ間の有線LAN",
    "cable_pc1": "PC①側の有線LAN",
    "cable_pc2": "PC②側の有線LAN",
}


DEVICE_ICONS = {
    "router": "📡",
    "hub_upper": "🔀",
    "hub_lower": "🔀",
    "pc1": "🖥️",
    "pc2": "🖥️",
    "cable_long": "➖",
    "cable_hubs": "➖",
    "cable_pc1": "➖",
    "cable_pc2": "➖",
}


DEVICE_ACTIONS = {
    device_id: [
        code for code, data in INVESTIGATIONS.items()
        if device_id in data["targets"]
    ]
    for device_id in DEVICE_LABELS
}


def initialize_state() -> None:
    defaults = {
        "screen": "title",
        "show_intro": False,
        "selected_device": None,
        "completed": [],
        "log": [],
        "finished": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_app() -> None:
    st.session_state.screen = "main"
    st.session_state.show_intro = True
    st.session_state.selected_device = None
    st.session_state.completed = []
    st.session_state.log = []
    st.session_state.finished = False


def reset_app() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def perform_investigation(code: str) -> None:
    if code in st.session_state.completed:
        return

    item = INVESTIGATIONS[code]
    st.session_state.completed.append(code)
    st.session_state.log.append(
        {
            "code": code,
            "title": item["title"],
            "result": item["result"],
            "meaning": item["meaning"],
        }
    )

    if len(st.session_state.completed) == len(INVESTIGATIONS):
        st.session_state.finished = True


@st.dialog("状況説明・アプリの使い方")
def intro_dialog() -> None:
    st.markdown(
        """
あなたは新しいパソコン（画面中の **PC②**）を買い、
自宅のローカル通信ネットワークに接続しました。

しかし、新しいパソコンでは通信障害が起きています。

**画面内の機器をクリックし、原因を特定しよう。**
"""
    )

    st.divider()
    st.markdown(
        """
### 使い方

1. PC・ハブ・有線LANなどをクリックします。
2. 表示された確認項目から、調べたいものを選びます。
3. 確認結果と「そこから分かること」を読み取ります。
4. すべての確認が終わると、シミュレーションは終了します。
"""
    )

    st.info(
        "この教材の目的は、正解を当てることではありません。"
        "正常な場所を確認し、原因候補を一つずつ除外する「切り分け」を体験することです。"
    )

    if st.button("調査を開始する", type="primary", use_container_width=True):
        st.session_state.show_intro = False
        st.rerun()


@st.dialog("調査終了")
def finish_dialog() -> None:
    st.markdown(
        """
## すべての確認が終わりました

今回の調査では、通信障害の原因を**一つに特定することはできませんでした**。

しかし、確認を重ねることで、原因候補を大きく絞り込むことができました。
"""
    )

    eliminated = []
    for code in st.session_state.completed:
        eliminated.extend(INVESTIGATIONS[code]["eliminates"])

    for item in dict.fromkeys(eliminated):
        st.write(f"✅ {item}")

    st.success(
        "原因を特定できなかったことは失敗ではありません。"
        "どこが正常かを確かめ、原因候補を切り分けられたことが今回の成果です。"
    )

    if st.button("タイトルへ戻る", use_container_width=True):
        reset_app()


def device_button(device_id: str, compact: bool = False) -> None:
    icon = DEVICE_ICONS[device_id]
    label = DEVICE_LABELS[device_id]
    selected = st.session_state.selected_device == device_id
    prefix = "▶ " if selected else ""

    if st.button(
        f"{prefix}{icon} {label}",
        key=f"device_{device_id}",
        use_container_width=True,
    ):
        st.session_state.selected_device = device_id
        st.rerun()

    if compact:
        st.caption("クリックして確認")


def render_network_map() -> None:
    st.markdown(
        """
<style>
.network-area {
    border: 1px solid #31546a;
    border-radius: 20px;
    padding: 18px;
    background: linear-gradient(180deg, #07131c, #0b1d29);
}
.route-label {
    text-align: center;
    color: #9ec4d8;
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
}
.arrow-text {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 800;
    color: #8ec8e8;
}
.bad-status {
    color: #ff7676;
    text-align: center;
    font-weight: 800;
    margin-top: -0.3rem;
}
.good-status {
    color: #77d99b;
    text-align: center;
    font-weight: 800;
    margin-top: -0.3rem;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="network-area">', unsafe_allow_html=True)

    top = st.columns([1.05, 0.75, 1.05, 0.75, 1.05], vertical_alignment="center")

    with top[0]:
        device_button("router")

    with top[1]:
        st.markdown("<div class='route-label'>長い有線LAN</div>", unsafe_allow_html=True)
        device_button("cable_long", compact=True)

    with top[2]:
        device_button("hub_upper")

    with top[3]:
        st.markdown("<div class='route-label'>ハブ間LAN</div>", unsafe_allow_html=True)
        device_button("cable_hubs", compact=True)

    with top[4]:
        device_button("hub_lower")

    st.markdown(
        "<div class='arrow-text'>ホームルーター　→　上流側ハブ　→　下流側ハブ</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    bottom = st.columns([0.7, 1.05, 0.7, 1.05], vertical_alignment="center")

    with bottom[0]:
        device_button("cable_pc1", compact=True)

    with bottom[1]:
        device_button("pc1")
        st.markdown("<div class='good-status'>通信可能</div>", unsafe_allow_html=True)

    with bottom[2]:
        device_button("cable_pc2", compact=True)

    with bottom[3]:
        device_button("pc2")
        st.markdown(
            "<div class='bad-status'>インターネットに接続できない</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_investigation_panel() -> None:
    st.subheader("確認する場所")

    selected = st.session_state.selected_device
    if selected is None:
        st.info("ネットワーク図の機器または有線LANをクリックしてください。")
        return

    st.markdown(f"### {DEVICE_ICONS[selected]} {DEVICE_LABELS[selected]}")

    for code in DEVICE_ACTIONS[selected]:
        item = INVESTIGATIONS[code]
        done = code in st.session_state.completed

        if st.button(
            ("✅ " if done else "🔎 ") + item["title"],
            key=f"action_{selected}_{code}",
            disabled=done or st.session_state.finished,
            use_container_width=True,
        ):
            perform_investigation(code)
            st.rerun()


def render_progress() -> None:
    completed = len(st.session_state.completed)
    total = len(INVESTIGATIONS)

    st.subheader("切り分けの進行状況")
    st.progress(completed / total)
    st.write(f"{completed} / {total} 項目を確認済み")

    eliminated = []
    for code in st.session_state.completed:
        eliminated.extend(INVESTIGATIONS[code]["eliminates"])

    st.markdown("#### 可能性が低くなった原因")
    if not eliminated:
        st.caption("調査を進めると、ここに切り分け結果が表示されます。")
    else:
        for item in dict.fromkeys(eliminated):
            st.write(f"✅ {item}")


def render_log() -> None:
    st.subheader("調査記録")

    if not st.session_state.log:
        st.caption("まだ調査を行っていません。")
        return

    for index, entry in enumerate(reversed(st.session_state.log), start=1):
        number = len(st.session_state.log) - index + 1

        with st.expander(
            f"{number}. {entry['title']}",
            expanded=(index == 1),
        ):
            st.markdown("**確認結果**")
            st.write(entry["result"])

            st.markdown("**この結果から分かること**")
            st.info(entry["meaning"])


def render_title() -> None:
    st.markdown(
        """
<style>
.stApp {
    background:
        radial-gradient(circle at 50% 25%, #17354d 0%, #08131e 42%, #02070c 100%);
}
.title-wrap {
    min-height: 70vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.title-card {
    width: min(860px, 92vw);
    padding: 62px 38px;
    border: 2px solid rgba(80, 185, 255, 0.7);
    border-radius: 28px;
    background: rgba(3, 15, 25, 0.88);
    box-shadow: 0 0 46px rgba(33, 148, 220, 0.25);
    text-align: center;
}
.title-small {
    color: #b8dcf2;
    font-size: 1.45rem;
    font-weight: 700;
}
.title-main {
    color: white;
    font-size: clamp(2.5rem, 6vw, 4.8rem);
    font-weight: 900;
    line-height: 1.2;
    margin-top: 12px;
}
.title-sub {
    color: #a9bfcc;
    margin-top: 24px;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="title-wrap">
  <div class="title-card">
    <div class="title-small">※本当にあった</div>
    <div class="title-main">通信障害診断<br>シミュレーター</div>
    <div class="title-sub">確認と比較を繰り返し、通信障害の原因を切り分けよう</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        if st.button(
            "画面をクリックしてスタート",
            type="primary",
            use_container_width=True,
        ):
            start_app()
            st.rerun()


def render_main() -> None:
    st.title(TITLE)
    st.caption("実際に起きた通信障害をもとに、原因の切り分けを体験します。")

    if st.button("状況説明をもう一度見る"):
        st.session_state.show_intro = True
        st.rerun()

    left, right = st.columns([1.75, 1], gap="large")

    with left:
        render_network_map()

    with right:
        render_investigation_panel()
        st.divider()
        render_progress()

    st.divider()
    render_log()

    if st.session_state.finished:
        finish_dialog()


st.set_page_config(
    page_title=TITLE,
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_state()

if st.session_state.screen == "title":
    render_title()
else:
    if st.session_state.show_intro:
        intro_dialog()
    render_main()
