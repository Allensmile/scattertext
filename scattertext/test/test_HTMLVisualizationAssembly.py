import sys
from unittest import TestCase

from scattertext.viz.HTMLVisualizationAssembly import HTMLVisualizationAssembly
from scattertext.viz.VizDataAdapter import VizDataAdapter


class TestHTMLVisualizationAssembly(TestCase):
	def get_params(self, param_dict={}):
		params = ['undefined', 'undefined', 'null', 'null', 'true', 'false', 'false', 'false']
		for i, val in param_dict.items():
			params[i] = val
		return 'buildViz(' + ','.join(params) + ');'

	def test_main(self):
		assembler = self.make_assembler()
		html = assembler.to_html()
		if sys.version_info.major == 2:
			self.assertEqual(type(html), unicode)
		else:
			self.assertEqual(type(html), str)
		self.assertFalse('<!-- INSERT SCRIPT -->' in html)
		self.assertTrue('Republican' in html)

	def test_protocol_is_https(self):
		html = self.make_assembler().to_html(protocol='https')
		self.assertTrue('https://' in html)
		self.assertFalse('http://' in html)

	def test_protocol_is_http(self):
		html = self.make_assembler().to_html(protocol='http')
		self.assertFalse('https://' in html)
		self.assertTrue('http://' in html)

	def test_protocol_defaults_to_http(self):
		self.assertEqual(self.make_assembler().to_html(protocol='http'),
		                 self.make_assembler().to_html(), )

	def test_raise_invalid_protocol_exception(self):
		with self.assertRaisesRegexp(BaseException,
		                             "Invalid protocol: ftp.  Protocol must be either http or https."):
			self.make_assembler().to_html(protocol='ftp')

	def test_height_width_default(self):
		assembler = self.make_assembler()
		self.assertEqual(assembler._call_build_visualization_in_javascript(), self.get_params())

	def test_color(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data, color='d3.interpolatePurples')
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({3: 'd3.interpolatePurples'}))

	def test_full_doc(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data, use_full_doc=True)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({5: 'true'}))

	def test_grey_zero_scores(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data, grey_zero_scores=True)
		                  ._call_build_visualization_in_javascript()), self.get_params({6: 'true'}))

	def test_chinese_mode(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data, chinese_mode=True)
		                  ._call_build_visualization_in_javascript()), self.get_params({7: 'true'}))


	def test_height_width_nondefault(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data, width_in_pixels=1000)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({0:'1000'}))

		self.assertEqual((HTMLVisualizationAssembly(visualization_data, height_in_pixels=60)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({1:'60'}))

		self.assertEqual((HTMLVisualizationAssembly(visualization_data,
		                                            height_in_pixels=60,
		                                            width_in_pixels=1000)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({0:'1000',1:'60'}))

	def test_max_snippets(self):
		visualization_data = self.make_adapter()
		self.assertEqual((HTMLVisualizationAssembly(visualization_data,
		                                            height_in_pixels=60,
		                                            width_in_pixels=1000,
		                                            max_snippets=None)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({0:'1000',1:'60'}))

		self.assertEqual((HTMLVisualizationAssembly(visualization_data,
		                                            height_in_pixels=60,
		                                            width_in_pixels=1000,
		                                            max_snippets=100)
		                  ._call_build_visualization_in_javascript()),
		                 self.get_params({0:'1000',1:'60', 2:'100'}))

	def make_assembler(self):
		visualization_data = self.make_adapter()
		assembler = HTMLVisualizationAssembly(visualization_data)
		return assembler

	def make_adapter(self):
		words_dict = {"info": {"not_category_name": "Republican", "category_name": "Democratic"},
		              "data": [{"y": 0.33763837638376387, "term": "crises", "ncat25k": 0,
		                        "cat25k": 1, "x": 0.0, "s": 0.878755930416447},
		                       {"y": 0.5, "term": "something else", "ncat25k": 0,
		                        "cat25k": 1, "x": 0.0,
		                        "s": 0.5}]}
		visualization_data = VizDataAdapter(words_dict)
		return visualization_data
