# Copyright 2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

from portage.tests import TestCase
from portage.tests.resolver.ResolverPlayground import ResolverPlayground, ResolverPlaygroundTestCase

class MultirepoTestCase(TestCase):

	def testMultirepo(self):
		ebuilds = {
			#Simple repo selection
			"dev-libs/A-1": { },
			"dev-libs/A-1::repo1": { },
			"dev-libs/A-2::repo1": { },
			"dev-libs/A-1::repo2": { },

			#Packges in exactly one repo
			"dev-libs/B-1": { },
			"dev-libs/C-1::repo1": { },

			#Package in repository 1 and 2, but 1 must be used
			"dev-libs/D-1::repo1": { },
			"dev-libs/D-1::repo2": { },

			"dev-libs/E-1": { },
			"dev-libs/E-1::repo1": { },
			"dev-libs/E-1::repo2": { "SLOT": "1" },

			"dev-libs/F-1::repo1": { "SLOT": "1" },
			"dev-libs/F-1::repo2": { "SLOT": "1" },
			}
		
		sets = {
			"multirepotest": 
				( "dev-libs/A::test_repo", )
		}

		test_cases = (
			#Simple repo selection
			ResolverPlaygroundTestCase(
				["dev-libs/A"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-2::repo1"]),
			ResolverPlaygroundTestCase(
				["dev-libs/A::test_repo"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-1"]),
			ResolverPlaygroundTestCase(
				["dev-libs/A::repo2"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-1::repo2"]),
			ResolverPlaygroundTestCase(
				["=dev-libs/A-1::repo1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-1::repo1"]),
			ResolverPlaygroundTestCase(
				["@multirepotest"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-1"]),

			#Packges in exactly one repo
			ResolverPlaygroundTestCase(
				["dev-libs/B"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/B-1"]),
			ResolverPlaygroundTestCase(
				["dev-libs/C"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/C-1::repo1"]),

			#Package in repository 1 and 2, but 2 must be used
			ResolverPlaygroundTestCase(
				["dev-libs/D"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/D-1::repo2"]),

			#Atoms with slots
			ResolverPlaygroundTestCase(
				["dev-libs/E"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/E-1::repo2"]),
			ResolverPlaygroundTestCase(
				["dev-libs/E:1::repo2"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/E-1::repo2"]),
			ResolverPlaygroundTestCase(
				["dev-libs/E:1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/E-1::repo2"]),
			ResolverPlaygroundTestCase(
				["dev-libs/F:1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/F-1::repo2"]),
			ResolverPlaygroundTestCase(
				["=dev-libs/F-1:1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/F-1::repo2"]),
			ResolverPlaygroundTestCase(
				["=dev-libs/F-1:1::repo1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/F-1::repo1"]),
			)

		playground = ResolverPlayground(ebuilds=ebuilds, sets=sets)
		try:
			for test_case in test_cases:
				playground.run_TestCase(test_case)
				self.assertEqual(test_case.test_success, True, test_case.fail_msg)
		finally:
			playground.cleanup()


	def testMultirepoUserConfig(self):
		ebuilds = {
			#package.use test
			"dev-libs/A-1": { "IUSE": "foo" },
			"dev-libs/A-2::repo1": { "IUSE": "foo" },
			"dev-libs/A-3::repo2": { },
			"dev-libs/B-1": { "DEPEND": "dev-libs/A", "EAPI": 2 },
			"dev-libs/B-2": { "DEPEND": "dev-libs/A[foo]", "EAPI": 2 },
			"dev-libs/B-3": { "DEPEND": "dev-libs/A[-foo]", "EAPI": 2 },

			#package.keywords test
			"dev-libs/C-1": { "KEYWORDS": "~x86" },
			"dev-libs/C-1::repo1": { "KEYWORDS": "~x86" },

			#package.license
			"dev-libs/D-1": { "LICENSE": "TEST" },
			"dev-libs/D-1::repo1": { "LICENSE": "TEST" },

			#package.mask
			"dev-libs/E-1": { },
			"dev-libs/E-1::repo1": { },
			"dev-libs/H-1": { },
			"dev-libs/H-1::repo1": { },

			#package.properties
			"dev-libs/F-1": { "PROPERTIES": "bar"},
			"dev-libs/F-1::repo1": { "PROPERTIES": "bar"},

			#package.unmask
			"dev-libs/G-1": { },
			"dev-libs/G-1::repo1": { },
			}

		user_config = {
			"package.use":
				(
					"dev-libs/A::repo1 foo",
				),
			"package.keywords":
				(
					"=dev-libs/C-1::test_repo",
				),
			"package.license":
				(
					"=dev-libs/D-1::test_repo TEST",
				),
			"package.mask":
				(
					"dev-libs/E::repo1",
					"dev-libs/H",
					#needed for package.unmask test
					"dev-libs/G",
				),
			"package.properties":
				(
					"dev-libs/F::repo1 -bar",
				),
			"package.unmask":
				(
					"dev-libs/G::test_repo",
				),
			}

		test_cases = (
			#package.use test
			ResolverPlaygroundTestCase(
				["=dev-libs/B-1"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-3::repo2", "dev-libs/B-1"]),
			ResolverPlaygroundTestCase(
				["=dev-libs/B-2"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-2::repo1", "dev-libs/B-2"]),
			ResolverPlaygroundTestCase(
				["=dev-libs/B-3"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/A-1", "dev-libs/B-3"]),

			#package.keywords test
			ResolverPlaygroundTestCase(
				["dev-libs/C"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/C-1"]),

			#package.license test
			ResolverPlaygroundTestCase(
				["dev-libs/D"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/D-1"]),

			#package.mask test
			ResolverPlaygroundTestCase(
				["dev-libs/E"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/E-1"]),

			#package.properties test
			ResolverPlaygroundTestCase(
				["dev-libs/F"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/F-1"]),

			#package.mask test
			ResolverPlaygroundTestCase(
				["dev-libs/G"],
				success = True,
				check_repo_names = True,
				mergelist = ["dev-libs/G-1"]),
			ResolverPlaygroundTestCase(
				["dev-libs/H"],
				success = False),
			)

		playground = ResolverPlayground(ebuilds=ebuilds, user_config=user_config)
		try:
			for test_case in test_cases:
				playground.run_TestCase(test_case)
				self.assertEqual(test_case.test_success, True, test_case.fail_msg)
		finally:
			playground.cleanup()
