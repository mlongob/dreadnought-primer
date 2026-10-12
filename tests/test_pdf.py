from pathlib import Path

from builder.pdf import PDF_NAME, broken_images, chrome_args, find_chrome


def test_chrome_runs_headless_with_a_debugging_port_and_its_own_profile():
    args = chrome_args("chrome", 9333, "/tmp/profile")
    assert args[0] == "chrome" and "--headless=new" in args
    assert "--remote-debugging-port=9333" in args and "--user-data-dir=/tmp/profile" in args


def test_the_chrome_variable_wins(monkeypatch, tmp_path):
    fake = tmp_path / "my-chrome"
    fake.write_text("")
    monkeypatch.setenv("CHROME", str(fake))
    assert find_chrome() == str(fake)


def test_broken_images_are_read_from_the_page():
    assert broken_images('<html lang="en-GB" data-broken-images="0">') == 0
    assert broken_images('<html data-broken-images="3" lang="en">') == 3
    assert broken_images("<html>") is None


def test_the_page_links_the_pdf(result=None):
    from builder.render import build
    html = build(Path(__file__).resolve().parent.parent, None).html
    assert f'href="{PDF_NAME}"' in html


def test_big_card_scans_are_shrunk_to_print_size(tmp_path):
    import io
    import pikepdf
    from PIL import Image
    from builder.pdf import PRINT_WIDTH, shrink

    buf = io.BytesIO()
    Image.new("RGB", (672, 936), "steelblue").save(buf, "JPEG", quality=95)
    pdf = pikepdf.new()
    pdf.add_blank_page()
    image = pikepdf.Stream(pdf, buf.getvalue(), Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Image,
                           Width=672, Height=936, ColorSpace=pikepdf.Name.DeviceRGB, BitsPerComponent=8,
                           Filter=pikepdf.Name.DCTDecode)
    pdf.pages[0].Resources = pikepdf.Dictionary(XObject=pikepdf.Dictionary(Im0=image))
    path = tmp_path / "in.pdf"
    pdf.save(path)
    shrink(path)
    out = pikepdf.open(path)
    im = out.pages[0].Resources.XObject.Im0
    assert int(im.Width) == PRINT_WIDTH and int(im.Height) == round(936 * PRINT_WIDTH / 672)


def test_the_sidebar_and_the_phone_bar_have_a_pdf_button():
    from builder.render import build
    html = build(Path(__file__).resolve().parent.parent, None).html
    assert html.count('class="pdf-button"') == 2
